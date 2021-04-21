from functions.helpers.drive import DriveFunctions
import numpy as np
import pandas as pd
import rasterio
from area import area as Area
import os
from functions.helpers.cordinates import GridCal
from tqdm import tqdm
import sys
pd.options.mode.chained_assignment = None  # default='warn'
class CalculationFunctions():
    def __init__(self,):
        self.df=DriveFunctions()
        self.gc=GridCal()
    def calculate_LST(self,thermal,ndvi,island8):
        if island8:
            ML = 0.0003342
            AL = 0.1
            K1 = 774.8853
            K2 = 1321.0789
        else:
            ML = 0.0670870
            AL = -0.0670899972319603
            K1 = 666.0900268554688
            K2 = 1282.7099609375
        TOA=(ML * thermal) + AL
        BT = (K2 / (np.log10 (K1 / TOA) + 1)) - 273.15
        Pv = ((ndvi - np.min(ndvi)) / (np.max(ndvi) - np.min(ndvi)))**2
        e  = 0.004 * Pv + 0.986
        LST = (BT / (1 + (0.00115 * BT / 1.4388) * np.log10(e)))
        return LST
    def calculation_of_domain(self,red, nir, green = None, swir = None,thermal=None,island8=True,forest_limit=0,crop_limit1=0,crop_limit2=0,builtup_limit_1=0,builtup_limit_2=0): 
        result=[]
        #Calculate the forest area using band 4 and band 5 (nir and red)
        #calculate ndvi
        ndvi=np.where(
        ((nir+red)==0. ),
        0, 
        ((nir-red)/(nir+red)))
        forest=ndvi

        forest = np.where(
            forest <= forest_limit,
            0,
            forest
        )
        result.append(forest)

        #Calculate the crops area using band 4 and band 5 (nir and red)

        crops=ndvi

        crops = np.where(
            crops <= crop_limit1,
            0,
            crops
        )
        crops = np.where(
            # crops > 0.13,
            crops >crop_limit2,
            0,
            crops
        )
        result.append(crops)

        #Calculate the building area using band 3, band 4, band 5, band 6 and band 7 (green, red, nir , swir)
        ibi =np.where(
            ( ((2 * swir/(swir +nir)) + (nir/(nir + red)) + (green/(green + red))) == 0. ), 
            0, 
            ((2 * swir/(swir +nir)) - (nir/(nir + red)) + (green/(green + red))) / ((2 * swir/(swir +nir)) + (nir/(nir + red)) + (green/(green + red))))

        forest = np.where(
            ndvi <= crop_limit1,
            0,
            1
        )

        ibi = np.where(
            ibi < builtup_limit_1, 
            0, 
            ibi)

        result.append(ibi)


        burn = np.where(
                ((nir+swir)==0. ), 
                0, 
                ((nir-swir)/(nir+swir)))


        forest = np.where(
            ndvi <= builtup_limit_1,
            0,
            1
        )

        burn = np.where(
                forest == 1, 
                burn, 
                0)

        result.append(burn)

        lst=self.calculate_LST(thermal=thermal,ndvi=ndvi,island8=island8)
        result.append(lst)

        result.append(ndvi)
        return result
    def calculate_area(self,arr,area_per_pixel):
        count=np.count_nonzero(arr)
        if count==0:return 0
        else:return (count*area_per_pixel)
    def merge_two_dicts(self,x, y):
        """Given two dictionaries, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z
    # fun to add to ds
    def add_to_df(self,newdata,path):
        df=pd.read_csv(path, index_col=False)
        if newdata['AREA'][0] not in list(df['AREA']):
            df=df.append(pd.DataFrame(newdata),ignore_index=True)
            df.to_csv(path, index=False)
    def create_empty_dict_rows(self,new_row_common):
        new_forest_row  = self.merge_two_dicts(new_row_common,{})
        new_crop_row    = self.merge_two_dicts(new_row_common,{})
        new_builtup_row = self.merge_two_dicts(new_row_common,{})
        new_burn_row    = self.merge_two_dicts(new_row_common,{})
        new_lst_row     = self.merge_two_dicts(new_row_common,{})
        new_airtemp_row     = self.merge_two_dicts(new_row_common,{})
        new_ndvi_row = self.merge_two_dicts(new_row_common,{})
        new_runoff_row = self.merge_two_dicts(new_row_common,{})
        new_pdsi_row = self.merge_two_dicts(new_row_common,{})
        new_vpd_row = self.merge_two_dicts(new_row_common,{})
        new_water_defict_row = self.merge_two_dicts(new_row_common,{})
        return  new_forest_row,new_crop_row,new_builtup_row, \
        new_burn_row,new_lst_row,new_airtemp_row, \
        new_ndvi_row,new_runoff_row, \
        new_pdsi_row,\
        new_vpd_row,new_water_defict_row
        

    def readImages(self,region,area,year,grid,isl8,folder_id):
        print(f"Reading Image {region}_{area}_{year}_G{grid}")
        sys.stdout.flush()
        idaho_name=f"{region}_{area}_{year}_G{grid}__Idaho.tif"
        landsat_name=f"{region}_{area}_{year}_G{grid}.tif"

        if self.df.get_image(landsat_name,folder_id):
            landsat_image = rasterio.open(landsat_name)
        
        if self.df.get_image(idaho_name,folder_id):
            idaho_image = rasterio.open(idaho_name)

        if isl8:
            # ["B3","B4","B5","B6","B7","B10"]
            green     = landsat_image.read(3).astype('float64')
            red       = landsat_image.read(4).astype('float64')
            nir       = landsat_image.read(5).astype('float64')
            swir      = ((landsat_image.read(6).astype('float64')) + (landsat_image.read(7).astype('float64')))/2
            thermal   = landsat_image.read(10).astype('float64')
        else:
            # ["B2","B3","B4","B5","B7","B6_VCID_1"]
            green     = landsat_image.read(2).astype('float64')
            red       = landsat_image.read(3).astype('float64')
            nir       = landsat_image.read(4).astype('float64')
            swir      = ((landsat_image.read(5).astype('float64')) + (landsat_image.read(8).astype('float64')))/2
            thermal   = landsat_image.read(6).astype('float64')

        tmmx      = idaho_image.read(11).astype('float64')
        pdsi      = idaho_image.read(3).astype('float64')
        vpd       = idaho_image.read(14).astype('float64')
        ro        = idaho_image.read(6).astype('float64')
        def_      = idaho_image.read(2).astype('float64')

        os.remove(landsat_name)
        os.remove(idaho_name)
        return np.array([green,red,nir,swir,thermal,\
                tmmx,pdsi,vpd,ro,def_])
    def create_csv(self,years):
        # csv format for main csv
        main_data={
            'REGION':[], "AREA":[],
            'CO-ORDINATES':[],
            'TOTAL_AREA':[],
            'G0_AREA':[],
            'G1_AREA':[],
            'G2_AREA':[],
            'G3_AREA':[],
            'G4_AREA':[],
            'G5_AREA':[],
            'G6_AREA':[],
            'G7_AREA':[],
            'G8_AREA':[],
            'G9_AREA':[],
            'G10_AREA':[],
            'G11_AREA':[],
            'G12_AREA':[],
            'G13_AREA':[],
            'G14_AREA':[],
            'G15_AREA':[],
        }
        main_df=pd.DataFrame(main_data)
        forest_data={
            'REGION':[], "AREA":[],
        }
        crop_data={
            'REGION':[], "AREA":[],
        }
        builtup_data={
            'REGION':[], "AREA":[],
        }
        airtemp_data={
            'REGION':[], "AREA":[],
        }
        burn_data={
            'REGION':[], "AREA":[],
        }
        lst_data={
            'REGION':[], "AREA":[],
        }
        ndvi_data={
            'REGION':[], "AREA":[],
        }
        pdsi_data={
            'REGION':[], "AREA":[],
        }
        vpd_data={
            'REGION':[], "AREA":[],
        }
        runoff_data={
            'REGION':[], "AREA":[],
        }
        waterdeficit_data={
            'REGION':[], "AREA":[],
        }
        features={0:'FOREST',1:'CROP',2:'BUILTUP',3:'AIRTEMP',4:'LST',5:'BURN',6:"NDVI",7:"RUNOFF",8:"PDSI",9:"VPD",10:"WATER_DEFICIT"}
        for k,feature in features.items():
            temp=[]
            for year in years:
                for grid_no in range(0,16):
                    if k in range(3,11):
                        temp.append(f'{year}_{feature}_MEAN_G{grid_no}')
                        temp.append(f'{year}_{feature}_MEDIAN_G{grid_no}')
                        temp.append(f'{year}_{feature}_MIN_G{grid_no}')
                        temp.append(f'{year}_{feature}_MAX_G{grid_no}')
                    else:
                        temp.append(f'{year}_{feature}_G{grid_no}')
            if k==0:
                for x in temp:
                    forest_data[x]=[]
                forest_df=pd.DataFrame(forest_data)
            if k==1:
                for x in temp:
                    crop_data[x]=[]
                crop_df=pd.DataFrame(crop_data)
            if k==2:
                for x in temp:
                    builtup_data[x]=[]
                builtup_df=pd.DataFrame(builtup_data)
            if k==3:
                for x in temp:
                    airtemp_data[x]=[]
                airtemp_df=pd.DataFrame(airtemp_data)
            if k==4:
                for x in temp:
                    lst_data[x]=[]
                lst_df=pd.DataFrame(lst_data)
            if k==5:
                for x in temp:
                    burn_data[x]=[]
                burn_df=pd.DataFrame(burn_data)
            if k==6:
                for x in temp:
                    ndvi_data[x]=[]
                ndvi_df=pd.DataFrame(ndvi_data)
            if k==6:
                for x in temp:
                    ndvi_data[x]=[]
                ndvi_df=pd.DataFrame(ndvi_data)
            if k==7:
                for x in temp:
                    runoff_data[x]=[]
                runoff_df=pd.DataFrame(runoff_data)
            if k==8:
                for x in temp:
                    pdsi_data[x]=[]
                pdsi_df=pd.DataFrame(pdsi_data)
            if k==9:
                for x in temp:
                    vpd_data[x]=[]
                vpd_df=pd.DataFrame(vpd_data)
            if k==10:
                for x in temp:
                    waterdeficit_data[x]=[]
                waterdeficit_df=pd.DataFrame(waterdeficit_data)
        main_df_path='/main_data.csv'
        forest_df_path='/forest_data.csv'
        crop_df_path='/crop_data.csv'
        burn_df_path='/burn_data.csv'
        builtup_df_path='/builtup_data.csv'
        lst_df_path='/lst_data.csv'
        airtemp_df_path='/airtemp_data.csv'
        ndvi_df_path='/ndvi_data.csv'
        pdsi_df_path='/pdsi_data.csv'
        vpd_df_path='/vpd_data.csv'
        runoff_df_path='/runoff_data.csv'
        waterdeficit_df_path='/waterdeficit_data.csv'
        main_df.to_csv(main_df_path, index=False)
        forest_df.to_csv(forest_df_path, index=False)
        crop_df.to_csv(crop_df_path, index=False)
        burn_df.to_csv(burn_df_path, index=False)
        builtup_df.to_csv(builtup_df_path, index=False)
        lst_df.to_csv(lst_df_path, index=False)
        airtemp_df.to_csv(airtemp_df_path, index=False)

        ndvi_df.to_csv(ndvi_df_path, index=False)
        pdsi_df.to_csv(pdsi_df_path, index=False)
        vpd_df.to_csv(vpd_df_path, index=False)
        runoff_df.to_csv(runoff_df_path, index=False)
        waterdeficit_df.to_csv(waterdeficit_df_path, index=False)
        return [main_df_path,forest_df_path,crop_df_path,builtup_df_path,airtemp_df_path,lst_df_path,
                burn_df_path,ndvi_df_path,runoff_df_path,pdsi_df_path,vpd_df_path,waterdeficit_df_path]
        
    def genrate_ds(self,data,all_paths,folder_id,years):
        # years=[(((int(data['Year']))-3)-x) for x in range(0,10)][::-1]
        # flag for compeletion of main csv data
        flag2=False
        #create path
        # get dataation coordinates
        area=data['Co-ordinate']
        # genrate 4*4 grid of the coordinates
        elements=self.gc.grid(area)
        # calculate the total area of the gird
        total_area=Area({'type':'Polygon','coordinates':area})/1000000
        # create dict for new row in main df
        new_row_common={'AREA':[data['Area'].replace(" ", "_")],'REGION':[data['Region'].replace(" ", "_")]}
        new_main_df_row=self.merge_two_dicts(new_row_common,{'CO-ORDINATES':[data['Co-ordinate']],'TOTAL_AREA':[total_area]})
        new_forest_row,new_crop_row,new_builtup_row, \
        new_burn_row,new_lst_row,new_airtemp_row, \
        new_ndvi_row,new_runoff_row, \
        new_pdsi_row,\
        new_vpd_row,new_water_defict_row=self.create_empty_dict_rows(new_row_common)
        df_dict={0:new_forest_row,1:new_crop_row,2:new_builtup_row,3:new_airtemp_row,4:new_lst_row,5:new_burn_row,
                    6:new_ndvi_row,7:new_runoff_row,8:new_pdsi_row,9:new_vpd_row,10:new_water_defict_row}
        year_loop=tqdm(years)
        for year in year_loop:
            
            if year <=2013:
                #landsat 7
                isl8=False
                # define limits for calculations
                forest_limit=0.22
                crop_limit1=0.09
                crop_limit2=0.15
                builtup_limit_1=0
                builtup_limit_2=0
            else:
                #landsat 8
                isl8=True
                # define limits for calculations
                forest_limit= 0.18
                crop_limit1=0.07
                crop_limit2=0.17
                builtup_limit_1=0.2
                builtup_limit_2=0

            flag1=False
            
            
            print(f"{data['Region']}_{data['Area']}_{year}")
            sys.stdout.flush()
            for i in range(0,len(elements)):
            
                # calculate the total grid area
                grid_area=Area({'type':'Polygon','coordinates':[elements[i]]})/1000000
                new_main_df_row[f'G{i}_AREA']=[]
                new_main_df_row[f'G{i}_AREA'].append(grid_area)
                
                green,red,nir,swir,thermal,\
                tmmx,pdsi,vpd,ro,def_=self.readImages(region=data['Region'],area=data['Area'],year=year,grid=i,isl8=isl8,folder_id=folder_id)
                # if area per pixel is not calculated then calculate it
                if not flag1:
                    # calculate the area per pixel
                    area_per_pixel=grid_area/(green.shape[0]*green.shape[1])
                    # set the flag to true
                    flag1=True
                # calculate the required features
                forest,crops,builtup,burn,lst,ndvi=self.calculation_of_domain(
                    island8=isl8,
                    red = red,
                    nir = nir,
                    thermal=thermal,
                    green = green,
                    swir = swir,
                    forest_limit=forest_limit,
                    crop_limit1=crop_limit1,
                    crop_limit2=crop_limit2,
                    builtup_limit_1=builtup_limit_1,
                    builtup_limit_2=builtup_limit_2)
                feature_data=[forest,crops,builtup,tmmx,lst,burn,ndvi,ro,pdsi,vpd,def_]
                features={0:'FOREST',1:'CROP',2:'BUILTUP',3:'AIRTEMP',4:'LST',5:'BURN',
                            6:"NDVI",7:"RUNOFF",8:"PDSI",9:"VPD",10:"WATER_DEFICIT"}
                for (k,df), (_,feature) in zip(df_dict.items(), features.items()):
                    if k in range(3,11):
                        if f'{year}_{feature}_MEAN_G{i}' not in df:
                            df[f'{year}_{feature}_MEAN_G{i}']=[]
                        df[f'{year}_{feature}_MEAN_G{i}'].append(np.mean(feature_data[k]))

                        if f'{year}_{feature}_MEDIAN_G{i}' not in df:
                            df[f'{year}_{feature}_MEDIAN_G{i}']=[]
                        df[f'{year}_{feature}_MEDIAN_G{i}'].append(np.median(feature_data[k]))

                        if f'{year}_{feature}_MIN_G{i}' not in df:
                            df[f'{year}_{feature}_MIN_G{i}']=[]
                        df[f'{year}_{feature}_MIN_G{i}'].append(np.min(feature_data[k]))

                        if f'{year}_{feature}_MAX_G{i}' not in df:
                            df[f'{year}_{feature}_MAX_G{i}']=[]
                        df[f'{year}_{feature}_MAX_G{i}'].append(np.max(feature_data[k]))
                    else:
                        if f'{year}_{feature}_G{i}' not in df:
                            df[f'{year}_{feature}_G{i}']=[]
                        df[f'{year}_{feature}_G{i}'].append(self.calculate_area(feature_data[k],area_per_pixel))
            if not flag2:
                self.add_to_df(new_main_df_row,all_paths[0])
                flag2=True
        for df,path in zip(df_dict.values(),all_paths[1:]):
            self.add_to_df(df,path)
            
    def merge(self, all_paths,folder_name):
        forest=pd.read_csv(all_paths[1])
        final_forest = forest[["REGION","AREA"]]
        ll = 2
        hl = 18

        final_forest['forest_year_1']= forest.iloc[:, ll:hl].sum(axis=1)#forest_year_1
        final_forest['forest_year_2']= forest.iloc[:, ll+(16*1):hl+(16*1)].sum(axis=1)#forest_year_2
        final_forest['forest_year_3']= forest.iloc[:, ll+(16*2):hl+(16*2)].sum(axis=1)#forest_year_3
        final_forest['forest_year_4']= forest.iloc[:, ll+(16*3):hl+(16*3)].sum(axis=1)#forest_year_4
        final_forest['forest_year_5']= forest.iloc[:, ll+(16*4):hl+(16*4)].sum(axis=1)#forest_year_5
        final_forest['forest_year_6']= forest.iloc[:, ll+(16*5):hl+(16*5)].sum(axis=1)#forest_year_6
        final_forest['forest_year_7']= forest.iloc[:, ll+(16*6):hl+(16*6)].sum(axis=1)#forest_year_7
        final_forest['forest_year_8']= forest.iloc[:, ll+(16*7):hl+(16*7)].sum(axis=1)#forest_year_8
        final_forest['forest_year_9']= forest.iloc[:, ll+(16*8):hl+(16*8)].sum(axis=1)#forest_year_9
        final_forest['forest_year_10']= forest.iloc[:, ll+(16*9):hl+(16*9)].sum(axis=1)#forest_year_10
        final_forest=final_forest.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_forest.to_csv('/final_forest.csv',index=False)

        # Crops
        crops=pd.read_csv(all_paths[2])
        final_crops = crops[["REGION","AREA"]]
        ll = 2
        hl = 18

        final_crops['crops_year_1']= crops.iloc[:, ll:hl].sum(axis=1)#crops_year_1
        final_crops['crops_year_2']= crops.iloc[:, ll+(16*1):hl+(16*1)].sum(axis=1)#crops_year_2
        final_crops['crops_year_3']= crops.iloc[:, ll+(16*2):hl+(16*2)].sum(axis=1)#crops_year_3
        final_crops['crops_year_4']= crops.iloc[:, ll+(16*3):hl+(16*3)].sum(axis=1)#crops_year_4
        final_crops['crops_year_5']= crops.iloc[:, ll+(16*4):hl+(16*4)].sum(axis=1)#crops_year_5
        final_crops['crops_year_6']= crops.iloc[:, ll+(16*5):hl+(16*5)].sum(axis=1)#crops_year_6
        final_crops['crops_year_7']= crops.iloc[:, ll+(16*6):hl+(16*6)].sum(axis=1)#crops_year_7
        final_crops['crops_year_8']= crops.iloc[:, ll+(16*7):hl+(16*7)].sum(axis=1)#crops_year_8
        final_crops['crops_year_9']= crops.iloc[:, ll+(16*8):hl+(16*8)].sum(axis=1)#crops_year_9
        final_crops['crops_year_10']= crops.iloc[:, ll+(16*9):hl+(16*9)].sum(axis=1)#crops_year_10
        final_crops=final_crops.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_crops.to_csv('/final_crops.csv',index=False)

        # builtup
        builtup = pd.read_csv(all_paths[3])
        final_builtup = builtup[["REGION","AREA"]]

        ll = 2
        hl = 18

        final_builtup['builtup_year_1']= builtup.iloc[:, ll:hl].sum(axis=1)#builtup_year_1
        final_builtup['builtup_year_2']= builtup.iloc[:, ll+(16*1):hl+(16*1)].sum(axis=1)#builtup_year_2
        final_builtup['builtup_year_3']= builtup.iloc[:, ll+(16*2):hl+(16*2)].sum(axis=1)#builtup_year_3
        final_builtup['builtup_year_4']= builtup.iloc[:, ll+(16*3):hl+(16*3)].sum(axis=1)#builtup_year_4
        final_builtup['builtup_year_5']= builtup.iloc[:, ll+(16*4):hl+(16*4)].sum(axis=1)#builtup_year_5
        final_builtup['builtup_year_6']= builtup.iloc[:, ll+(16*5):hl+(16*5)].sum(axis=1)#builtup_year_6
        final_builtup['builtup_year_7']= builtup.iloc[:, ll+(16*6):hl+(16*6)].sum(axis=1)#builtup_year_7
        final_builtup['builtup_year_8']= builtup.iloc[:, ll+(16*7):hl+(16*7)].sum(axis=1)#builtup_year_8
        final_builtup['builtup_year_9']= builtup.iloc[:, ll+(16*8):hl+(16*8)].sum(axis=1)#builtup_year_9
        final_builtup['builtup_year_10']= builtup.iloc[:, ll+(16*9):hl+(16*9)].sum(axis=1)#builtup_year_10
        final_builtup=final_builtup.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_builtup.to_csv('/final_builtup.csv',index=False)

        # Air temp
        airtemp = pd.read_csv(all_paths[4])
        final_airtemp = airtemp[["REGION","AREA"]]

        final_airtemp['airtemp_year_1']= airtemp.iloc[:, 3:67:4].median(axis=1)#airtemp_year_1
        final_airtemp['airtemp_year_2']= airtemp.iloc[:, 67:131:4].median(axis=1)#airtemp_year_2
        final_airtemp['airtemp_year_3']= airtemp.iloc[:, 131:195:4].median(axis=1)#airtemp_year_3
        final_airtemp['airtemp_year_4']= airtemp.iloc[:, 195:259:4].median(axis=1)#airtemp_year_4
        final_airtemp['airtemp_year_5']= airtemp.iloc[:, 259:323:4].median(axis=1)#airtemp_year_5
        final_airtemp['airtemp_year_6']= airtemp.iloc[:, 323:387:4].median(axis=1)#airtemp_year_6
        final_airtemp['airtemp_year_7']= airtemp.iloc[:, 387:451:4].median(axis=1)#airtemp_year_7
        final_airtemp['airtemp_year_8']= airtemp.iloc[:, 451:515:4].median(axis=1)#airtemp_year_8
        final_airtemp['airtemp_year_9']= airtemp.iloc[:, 515:579:4].median(axis=1)#airtemp_year_9
        final_airtemp['airtemp_year_10']= airtemp.iloc[:, 579:642:4].median(axis=1)#airtemp_year_10
        final_airtemp=final_airtemp.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_airtemp.to_csv('/final_airtemp.csv',index=False)

        # Burn
        burn =  pd.read_csv(all_paths[6])
        final_burn = burn[["REGION","AREA"]]

        final_burn['burn_year_1']= burn.iloc[:, 3:67:4].median(axis=1)#burn_year_1
        final_burn['burn_year_2']= burn.iloc[:, 67:131:4].median(axis=1)#burn_year_2
        final_burn['burn_year_3']= burn.iloc[:, 131:195:4].median(axis=1)#burn_year_3
        final_burn['burn_year_4']= burn.iloc[:, 195:259:4].median(axis=1)#burn_year_4
        final_burn['burn_year_5']= burn.iloc[:, 259:323:4].median(axis=1)#burn_year_5
        final_burn['burn_year_6']= burn.iloc[:, 323:387:4].median(axis=1)#burn_year_6
        final_burn['burn_year_7']= burn.iloc[:, 387:451:4].median(axis=1)#burn_year_7
        final_burn['burn_year_8']= burn.iloc[:, 451:515:4].median(axis=1)#burn_year_8
        final_burn['burn_year_9']= burn.iloc[:, 515:579:4].median(axis=1)#burn_year_9
        final_burn['burn_year_10']= burn.iloc[:, 579:642:4].median(axis=1)#burn_year_10

        final_burn=final_burn.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_burn.to_csv('/final_burn.csv',index=False)

        # mainarea
        mainarea = pd.read_csv(all_paths[0])
        final_mainarea = mainarea[["REGION","AREA","TOTAL_AREA"]]
        final_mainarea=final_mainarea.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_mainarea.to_csv('/final_mainarea.csv',index=False)

        # pdsi
        pdsi = pd.read_csv(all_paths[9])
        final_pdsi = pdsi[["REGION","AREA"]]

        final_pdsi['pdsi_year_1']= pdsi.iloc[:, 3:67:4].median(axis=1)#pdsi_year_1
        final_pdsi['pdsi_year_2']= pdsi.iloc[:, 67:131:4].median(axis=1)#pdsi_year_2
        final_pdsi['pdsi_year_3']= pdsi.iloc[:, 131:195:4].median(axis=1)#pdsi_year_3
        final_pdsi['pdsi_year_4']= pdsi.iloc[:, 195:259:4].median(axis=1)#pdsi_year_4
        final_pdsi['pdsi_year_5']= pdsi.iloc[:, 259:323:4].median(axis=1)#pdsi_year_5
        final_pdsi['pdsi_year_6']= pdsi.iloc[:, 323:387:4].median(axis=1)#pdsi_year_6
        final_pdsi['pdsi_year_7']= pdsi.iloc[:, 387:451:4].median(axis=1)#pdsi_year_7
        final_pdsi['pdsi_year_8']= pdsi.iloc[:, 451:515:4].median(axis=1)#pdsi_year_8
        final_pdsi['pdsi_year_9']= pdsi.iloc[:, 515:579:4].median(axis=1)#pdsi_year_9
        final_pdsi['pdsi_year_10']= pdsi.iloc[:, 579:642:4].median(axis=1)#pdsi_year_10
        final_pdsi=final_pdsi.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_pdsi.to_csv('/final_pdsi.csv',index=False)

        # run_off
        runoff = pd.read_csv(all_paths[8])
        final_runoff = runoff[["REGION","AREA"]]
        final_runoff

        final_runoff['runoff_year_1']= runoff.iloc[:, 3:67:4].median(axis=1)#runoff_year_1
        final_runoff['runoff_year_2']= runoff.iloc[:, 67:131:4].median(axis=1)#runoff_year_2
        final_runoff['runoff_year_3']= runoff.iloc[:, 131:195:4].median(axis=1)#runoff_year_3
        final_runoff['runoff_year_4']= runoff.iloc[:, 195:259:4].median(axis=1)#runoff_year_4
        final_runoff['runoff_year_5']= runoff.iloc[:, 259:323:4].median(axis=1)#runoff_year_5
        final_runoff['runoff_year_6']= runoff.iloc[:, 323:387:4].median(axis=1)#runoff_year_6
        final_runoff['runoff_year_7']= runoff.iloc[:, 387:451:4].median(axis=1)#runoff_year_7
        final_runoff['runoff_year_8']= runoff.iloc[:, 451:515:4].median(axis=1)#runoff_year_8
        final_runoff['runoff_year_9']= runoff.iloc[:, 515:579:4].median(axis=1)#runoff_year_9
        final_runoff['runoff_year_10']= runoff.iloc[:, 579:642:4].median(axis=1)#runoff_year_10

        final_runoff=final_runoff.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_runoff.to_csv('/final_runoff.csv',index=False)

        # vpd
        vpd = pd.read_csv(all_paths[10])
        final_vpd = vpd[["REGION","AREA"]]
        final_vpd['vpd_year_1']= vpd.iloc[:, 3:67:4].median(axis=1)#vpd_year_1
        final_vpd['vpd_year_2']= vpd.iloc[:, 67:131:4].median(axis=1)#vpd_year_2
        final_vpd['vpd_year_3']= vpd.iloc[:, 131:195:4].median(axis=1)#vpd_year_3
        final_vpd['vpd_year_4']= vpd.iloc[:, 195:259:4].median(axis=1)#vpd_year_4
        final_vpd['vpd_year_5']= vpd.iloc[:, 259:323:4].median(axis=1)#vpd_year_5
        final_vpd['vpd_year_6']= vpd.iloc[:, 323:387:4].median(axis=1)#vpd_year_6
        final_vpd['vpd_year_7']= vpd.iloc[:, 387:451:4].median(axis=1)#vpd_year_7
        final_vpd['vpd_year_8']= vpd.iloc[:, 451:515:4].median(axis=1)#vpd_year_8
        final_vpd['vpd_year_9']= vpd.iloc[:, 515:579:4].median(axis=1)#vpd_year_9
        final_vpd['vpd_year_10']= vpd.iloc[:, 579:642:4].median(axis=1)#vpd_year_10
        final_vpd=final_vpd.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_vpd.to_csv('/final_vpd.csv',index=False)

        # final_waterdeficit
        waterdeficit = pd.read_csv(all_paths[11])
        final_waterdeficit = waterdeficit[["REGION","AREA"]]
        
        final_waterdeficit['waterdeficit_year_1']= waterdeficit.iloc[:, 3:67:4].median(axis=1)#waterdeficit_year_1
        final_waterdeficit['waterdeficit_year_2']= waterdeficit.iloc[:, 67:131:4].median(axis=1)#waterdeficit_year_2
        final_waterdeficit['waterdeficit_year_3']= waterdeficit.iloc[:, 131:195:4].median(axis=1)#waterdeficit_year_3
        final_waterdeficit['waterdeficit_year_4']= waterdeficit.iloc[:, 195:259:4].median(axis=1)#waterdeficit_year_4
        final_waterdeficit['waterdeficit_year_5']= waterdeficit.iloc[:, 259:323:4].median(axis=1)#waterdeficit_year_5
        final_waterdeficit['waterdeficit_year_6']= waterdeficit.iloc[:, 323:387:4].median(axis=1)#waterdeficit_year_6
        final_waterdeficit['waterdeficit_year_7']= waterdeficit.iloc[:, 387:451:4].median(axis=1)#waterdeficit_year_7
        final_waterdeficit['waterdeficit_year_8']= waterdeficit.iloc[:, 451:515:4].median(axis=1)#waterdeficit_year_8
        final_waterdeficit['waterdeficit_year_9']= waterdeficit.iloc[:, 515:579:4].median(axis=1)#waterdeficit_year_9
        final_waterdeficit['waterdeficit_year_10']= waterdeficit.iloc[:, 579:642:4].median(axis=1)#waterdeficit_year_10

        final_waterdeficit=final_waterdeficit.drop_duplicates(subset=['AREA','REGION'], keep="last", inplace=False)
        final_waterdeficit.to_csv('/final_waterdeficit.csv',index=False)

        all_main_paths = [
                            "/final_mainarea.csv",
                            "/final_forest.csv",
                            "/final_crops.csv",
                            "/final_burn.csv",
                            "/final_airtemp.csv",
                            "/final_pdsi.csv",
                            "/final_runoff.csv",
                            "/final_vpd.csv",
                            "/final_waterdeficit.csv",
        ]
        df = mainarea[["REGION","AREA"]]
        for path in all_main_paths:
            temp=pd.read_csv(path,index_col=False)
            df = pd.merge(df, temp,  how='left', left_on=['AREA','REGION'], right_on =['AREA','REGION'])
        df.to_csv(f'{folder_name}.csv', index=False)
        return '{folder_name}.csv'