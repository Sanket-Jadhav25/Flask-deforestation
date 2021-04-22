from datetime import datetime

from googleapiclient.http import MediaFileUpload
import pandas as pd
from functions.helpers.email_ import Email
from functions.helpers.report import Report
from functions.helpers.predict import Predict
from functions.helpers.calculation import CalculationFunctions
from functions.helpers.download import Download_Images
from functions.helpers.drive import DriveFunctions

import os
from dotenv import load_dotenv
import sys
def download_images(data):
    load_dotenv()
    
    # driveFolderID=os.getenv('driveFolderID')
    years=[(((int(data['Year']))-3)-x) for x in range(0,10)][::-1]
    df=DriveFunctions()
    # folder_name=f"{data['User']}-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # dwn=Download_Images()
    # temp_folder_name=f"temp_{folder_name}"
    # temp_drive_folderID=df.create_folder(temp_folder_name)
    
    # dwn.download(data,years,destination_folder=temp_folder_name)
    
    # folder_id=dwn.check_and_download(temp_drive_folderID,data,folder_name,driveFolderID)
    folder_id='1Y3gIldKi9C-V1XZFk7u_OThAJpZUJYz9'
    folder_name='omkar-2021-04-22_13-49-43'
    if folder_id:
        cf=CalculationFunctions()
        all_paths=cf.create_csv(years)
        print('Created CSV')
        sys.stdout.flush()
        cf.genrate_ds(data,all_paths,folder_id,years)
        print("Genrated Dataset")
        sys.stdout.flush()
        path,forest=cf.merge(all_paths,folder_name)
        fileId=df.upload_file(path,folder_id)
        print("Merged Dataset")
        sys.stdout.flush()
        print(forest)
        sys.stdout.flush()
        #predict
        pred=Predict(os.path.abspath(os.path.join(os.getcwd(),os.getenv('model_path'))))
        predictions=pred.predict(forest)
        print(predictions)
        sys.stdout.flush()
        rp=Report()
        report_path=report_path=rp.create_report(predictions[0][0],forest,data,years)
        email=os.getenv('email')
        password=os.getenv('password')
        em=Email(email,password)
        subject=f"Report for {data['Region']} {data['Area']}"
        mail_content=''
        em.send_email(reciver=data['Email'],subject=subject,content=mail_content,files=[report_path])
        
        
        
