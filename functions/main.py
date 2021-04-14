
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
    # driveId=os.getenv('driveId')
    driveFolderID=os.getenv('driveFolderID')

    # dwn=Download_Images()

    # dwn.download(data)
    # folder_id=dwn.check_and_download(temp_drive_folderID,data,driveFolderID)
    
    folder_id='16kGWNe3fOKum_8IVNmaCZkGOJKto5e2L'
    if folder_id:
    #     #extract features
        cf=CalculationFunctions()
        all_paths=cf.create_csv()
        print('Created CSV')
        sys.stdout.flush()
        cf.genrate_ds(data,all_paths,folder_id)
        print("Genrated Dataset")
        sys.stdout.flush()
        df=cf.merge(all_paths)
        print("Merged Dataset")
        sys.stdout.flush()
        print(df)
        sys.stdout.flush()
        #predict
        # pred=Predict('path to model')
        # predictions=pred.predict(df)
        # rp=Report()
        # #TODO
        # rp.create_report(predictions)
        
        
        
