from datetime import datetime
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
    
    driveFolderID=os.getenv('driveFolderID')
    years=[(((int(data['Year']))-3)-x) for x in range(0,10)][::-1]
    df=DriveFunctions()
    folder_name=f"{data['User']}-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    dwn=Download_Images()
    temp_drive_folderID=df.create_folder(f"temp_{folder_name}")
    dwn.download(data,years,destination_folder=temp_drive_folderID)
    folder_id=dwn.check_and_download(temp_drive_folderID,data,folder_name,driveFolderID)
    if folder_id:
        cf=CalculationFunctions()
        all_paths=cf.create_csv(years)
        print('Created CSV')
        sys.stdout.flush()
        cf.genrate_ds(data,all_paths,folder_id,years)
        print("Genrated Dataset")
        sys.stdout.flush()
        all_paths=['/main_data.csv',
                '/forest_data.csv',
                '/crop_data.csv',
                '/builtup_data.csv',
                '/airtemp_data.csv',
                '/lst_data.csv',
                '/burn_data.csv',
                '/ndvi_data.csv',
                '/runoff_data.csv',
                '/pdsi_data.csv',
                '/vpd_data.csv',
                '/waterdeficit_data.csv']
        df=cf.merge(all_paths)
        print("Merged Dataset")
        sys.stdout.flush()
        print(df)
        sys.stdout.flush()
        #predict
        pred=Predict(os.path.abspath(os.path.join(os.getcwd(),os.getenv('model_path'))))
        predictions=pred.predict(df)
        print(predictions)
        sys.stdout.flush()
        rp=Report()
        # #TODO
        rp.create_report(predictions=predictions,csv=df,path=f'reports/{folder_name}.pdf')
        email=os.getenv('email')
        password=os.getenv('password')
        em=Email(email,password)
        subject=f"Report for {data['Region']} {data['Area']}"
        mail_content=''
        em.send_email(reciver=data['email'],subject=subject,content=mail_content,files=[f'reports/{folder_name}.pdf'])
        
        
        
