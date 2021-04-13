from functions.helpers.cordinates import GridCal
from functions.helpers.missing import FillMissing
from functions.helpers.earth_engine import EarthEngineFunctions
from functions.helpers.drive import DriveFunctions
from tqdm import tqdm
import sys
class Download_Images():
  def __init__(self,):
    self.eef=EarthEngineFunctions()
    self.df=DriveFunctions()
    self.gc=GridCal()
    self.fm=FillMissing(self.eef,self.df,self.gc)
    
  def temp(self,data):
    print(self.eef.ee.Geometry.Polygon(data['Co-ordinate'], None, False))
    sys.stdout.flush() 
  def download(self,data):
    print('Downloading')
    sys.stdout.flush() 
    years=[(x+2007) for x in range(0,10)]
    destination_folder="LandsatImages"
    # get data coordinates
    area=data['Co-ordinate']
    # genrate 4*4 grid of the coordinates
    elements=self.gc.grid(area)
    # create earth engine geometry if the area
    area=self.eef.ee.Geometry.Polygon(area, None, False)
    # create dict for new row in main df
    print('Years Done:')
    sys.stdout.flush() 
    year_loop=tqdm(years)
    for year in year_loop:
      print(f'Year Selected {year}:')
      sys.stdout.flush() 
      sys.stdout.flush() 
      startDate =self.eef.ee.Date.fromYMD(year,1,1)
      endDate =self.eef.ee.Date.fromYMD(year,12,31)
      if year <=2013:
        landsatDS="LANDSAT/LE07/C01/T1"
        landsatBands=["B2","B3","B4","B5","B7","B6_VCID_1"]
      else:
        landsatDS="LANDSAT/LC08/C01/T1"
        landsatBands=["B3","B4","B5","B6","B7","B10"]
      IdahoDS="IDAHO_EPSCOR/TERRACLIMATE"
      IdahoBands=["tmmx","pdsi","vpd","ro","def"]
      ee_image_landsat=self.eef.getGEEDataset(name=landsatDS,startDate=startDate,endDate=endDate,area=area,bands=landsatBands)
      ee_image_Idaho=self.eef.getGEEDataset(name=IdahoDS,startDate=startDate,endDate=endDate,area=area,bands=IdahoBands)

      print('Grid Progress:')
      sys.stdout.flush() 
      inner_loop=tqdm(range(0,len(elements)))
      inner_loop.reset()
      for i in inner_loop:
        print(f"{data['Region']}_{data['Area']}_{year}_G{i}_Idaho")
        sys.stdout.flush() 
        name=f"{data['Region']}_{data['Area']}_{year}_G{i}__Idaho"
        # self.eef.drive_transfer(img=ee_image_Idaho,name=name,cord=elements[i],band_list=IdahoBands,destination_folder=destination_folder)
        print(f"{data['Region']}_{data['Area']}_{year}_G{i}")
        sys.stdout.flush() 
        name=f"{data['Region']}_{data['Area']}_{year}_G{i}"
        # self.eef.drive_transfer(img=ee_image_landsat,name=name,cord=elements[i],band_list=landsatBands,destination_folder=destination_folder)
      print(f'Year {year} Done!')
      sys.stdout.flush() 

  def check_and_download(self,folder,data,driveFolderID):
      total_size=320
      files=self.df.get_files(folder)
      ATTEMPTES=5
      while len(files)!=total_size and ATTEMPTES!=0: 
        missing_years=self.fm.find_missing_years(files)
        for year in missing_years:
          year_data=[f for f in files if str(year) in f['name']]
          missing_grids=self.fm.find_missing_grid(year_data)
          for grid in missing_grids:
            self.fm.download_missing_data(year,grid,data)
        files=self.df.get_files(folder)
        ATTEMPTES=ATTEMPTES-1
      if len(files)!=total_size:
        return False
      else:return self.df.create_folder_and_move(data['User'],driveFolderID,files)