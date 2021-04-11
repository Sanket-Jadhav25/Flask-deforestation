import os

from dotenv.main import load_dotenv
from functions.helpers.authenticate import authenticate_ee
import time
class EarthEngineFunctions():
  def __init__(self,path_to_env):
    load_dotenv(dotenv_path=path_to_env)
    service_account = os.getenv('service_account')
    file_path=os.getenv('service_account_file_path')
    self.ee=authenticate_ee(file_path=file_path,service_account=service_account)

  def getGEEDataset(self,name,startDate,endDate,area,bands):
    # select collection with date range and filter bounds
    imgCollection=self.ee.ImageCollection(name).filterDate(startDate,endDate)
    # for band in bands:
    #   imgCollection=imgCollection.filter(ee.Filter.neq(band, None))
    # create image of the collection
    img = self.ee.Image(imgCollection.median())
    # select the needed bands
    # img_full = img.select(ee.List(bands))
    return img

  def drive_transfer(self,img,name,cord,band_list,destination_folder):
  # Specify patch and file dimensions.
  #   image_export_options = {
  #     'patchDimensions': [256, 256],
  #     'maxFileSize': 104857600,
  #     'compressed': True
  #   }

    # Setup the task.
    image_task = self.ee.batch.Export.image.toDrive(
      image=img,
      description= name,
      fileNamePrefix= name,
      scale=30,
      fileFormat='GeoTiff',
      region=cord,
      folder= destination_folder,
      formatOptions={
              "cloudOptimized": True
      },
    )
    image_task.start()
    # Block until the task completes.
    print('Running image export to Drive Storage...')
    while image_task.active():
      time.sleep(5)

    # Error condition
    if image_task.status()['state'] != 'COMPLETED':
      print('Error with image export.')
    else:
      print('Image export completed.')
    return None