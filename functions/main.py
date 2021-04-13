
from functions.helpers.report import Report
# from functions.helpers.predict import Predict
from functions.helpers.calculation import CalculationFunctions
from functions.helpers.download import Download_Images
import os
from dotenv import load_dotenv
import sys
# filename = os.path.join(dirname, 'relative/path/to/file/you/want')
def download_images(data):
    load_dotenv()
    
    temp_drive_folderID=os.getenv('temp_drive_folderID')
    driveId=os.getenv('driveId')
    driveFolderID=os.getenv('driveFolderID')

    dwn=Download_Images()

    dwn.temp(data)
    # folder_id=dwn.check_and_download(temp_drive_folderID,data,driveFolderID)
    # if folder_id:
    #     #extract features
    #     cf=CalculationFunctions('secrets\.env')
    #     all_paths=cf.create_csv()
    #     cf.genrate_ds(data,all_paths,folder_id)
    #     df=cf.merge(all_paths)
    #     print(df)
    #     #predict
    #     # pred=Predict('path to model')
    #     # predictions=pred.predict(df)
    #     # rp=Report()
    #     # #TODO
    #     # rp.create_report(predictions)
        
        
        
