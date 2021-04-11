
from functions.helpers.download import Download_Images
import os
from dotenv import load_dotenv

def download_images(data):
    temp_drive_folderID=os.getenv('temp_drive_folderID')
    # driveId=os.getenv('driveId')
    driveFolderID=os.getenv('driveFolderID')
    dwn=Download_Images('secrets\.env')
    dwn.download(data)
    folder_id=dwn.check_and_download(temp_drive_folderID,data,driveFolderID)
    if folder_id:
        #extract features
        pass
