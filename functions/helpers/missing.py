import ee
from tqdm import tqdm


class FillMissing():
  def __init__(self,eef,df,gc):
    self.eef=eef
    self.df=df
    self.gc=gc
      
  def check_missing(self,files):
    a=[0]*11
    for r in files:
      if '2007' in r['name']:
        a[0]=a[0]+1
      elif '2008' in r['name']:
        a[1]=a[1]+1
      elif '2009' in r['name']:
        a[2]=a[2]+1
      elif '2010' in r['name']:
        a[3]=a[3]+1
      elif '2011' in r['name']:
        a[4]=a[4]+1
      elif '2012' in r['name']:
        a[5]=a[5]+1
      elif '2013' in r['name']:
        a[6]=a[6]+1
      elif '2014' in r['name']:
        a[7]=a[7]+1
      elif '2015' in r['name']:
        a[8]=a[8]+1
      elif '2016' in r['name']:
        a[9]=a[9]+1
      else:
        a[10]=a[10]+1
      return a


  def find_missing_years(self,files):
    missing_array=self.check_missing(files)
    if missing_array[10]!=0:
      raise Exception('Gadbad')
    else:
      error=[]
      for i,v in enumerate(missing_array[:10]):
        if v!=32:
          error.append(2007+i)
      return error


  def find_missing_grid(self,year_data):
    a=[0]*16
    for r in year_data:
      if 'G0.' in r['name'] or 'G0_' in r['name']:
        a[0]=a[0]+1
      elif 'G1.' in r['name'] or 'G1_' in r['name']:
        a[1]=a[1]+1
      elif 'G2.' in r['name'] or 'G2_' in r['name']:
        a[2]=a[2]+1
      elif 'G3.' in r['name'] or 'G3_' in r['name']:
        a[3]=a[3]+1
      elif 'G4.' in r['name'] or 'G4_' in r['name']:
        a[4]=a[4]+1
      elif 'G5.' in r['name'] or 'G5_' in r['name']:
        a[5]=a[5]+1
      elif 'G6.' in r['name'] or 'G6_' in r['name']:
        a[6]=a[6]+1
      elif 'G7.' in r['name'] or 'G7_' in r['name']:
        a[7]=a[7]+1
      elif 'G8.' in r['name'] or 'G8_' in r['name']:
        a[8]=a[8]+1
      elif 'G9.' in r['name'] or 'G9_' in r['name']:
        a[9]=a[9]+1
      elif 'G10.' in r['name'] or 'G10_' in r['name']:
        a[10]=a[10]+1
      elif 'G11' in r['name'] or 'G11_' in r['name']:
        a[11]=a[11]+1
      elif 'G12.' in r['name'] or 'G12_' in r['name']:
        a[12]=a[12]+1
      elif 'G13.' in r['name'] or 'G13_' in r['name']:
        a[13]=a[13]+1
      elif 'G14.' in r['name'] or 'G14_' in r['name']:
        a[14]=a[14]+1
      elif 'G15.' in r['name'] or 'G15_' in r['name']:
        a[15]=a[15]+1

    errors=[]
    for i,v in enumerate(a):
      if v!=2:
        errors.append(i)
    return a


  def download_specific(self,data,year,grid_no,landsat=True):
    destination_folder="LandsatImages"
    # get data coordinates
    area=data['Co-ordinate']
    # genrate 4*4 grid of the coordinates
    elements=self.gc.grid(area)
    # create earth engine geometry if the area
    area=self.eef.ee.Geometry.Polygon(area, None, False)
    # create dict for new row in main df
    print('Years Done:')
    year_loop=tqdm([year])
    for year in year_loop:
      print(f'Year Selected {year}:')
      startDate =self.eef.ee.Date.fromYMD(year,1,1)
      endDate =self.eef.ee.Date.fromYMD(year,12,31)
      if landsat:
        if year <=2013:
          landsatDS="LANDSAT/LE07/C01/T1"
          landsatBands=["B2","B3","B4","B5","B7","B6_VCID_1"]
        else:
          landsatDS="LANDSAT/LC08/C01/T1"
          landsatBands=["B3","B4","B5","B6","B7","B10"]
        ee_image_landsat=self.eef.getGEEDataset(name=landsatDS,startDate=startDate,endDate=endDate,area=area,bands=landsatBands)
        print(f"{data['Region']}_{data['Area']}_{year}_G{grid_no}")
        name=f"{data['Region']}_{data['Area']}_{year}_G{grid_no}"
        self.eef.drive_transfer(img=ee_image_landsat,name=name,cord=elements[grid_no],band_list=landsatBands,destination_folder=destination_folder)
      else:
        IdahoDS="IDAHO_EPSCOR/TERRACLIMATE"
        IdahoBands=["tmmx","pdsi","vpd","ro","def"]
        ee_image_Idaho=self.eef.getGEEDataset(name=IdahoDS,startDate=startDate,endDate=endDate,area=area,bands=IdahoBands)
        print(f"{data['Region']}_{data['Area']}_{year}_G{grid_no}_Idaho")
        name=f"{data['Region']}_{data['Area']}_{year}_G{grid_no}__Idaho"
        self.eef.drive_transfer(img=ee_image_Idaho,name=name,cord=elements[grid_no],band_list=IdahoBands,destination_folder=destination_folder)
      print(f'Year {year} Done!')

  def download_missing_data(self,year,grid,data):
    landsat=f"{data['Region']}_{data['Area']}_{year}_G{grid}.tif"
    idhao=f"{data['Region']}_{data['Area']}_{year}_G{grid}__Idaho.tif"
    if not self.df.find_file(landsat):
      self.download_specific(data,year,grid,landsat=True)
    elif not self.df.find_file(idhao):
      self.download_specific(data,year,grid,landsat=False)


