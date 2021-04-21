from google.oauth2 import service_account
# import ee
from apiclient import discovery

def authenticate_ee(file_path,service_account):  
  
  credentials = ee.ServiceAccountCredentials(service_account, file_path)
  ee.Initialize(credentials)
  return ee

def authenticate_drive(file_path):  
  SCOPES = [
        'https://www.googleapis.com/auth/drive'
    ]
  credentials = service_account.Credentials.from_service_account_file(
            file_path, scopes=SCOPES)
  service = discovery.build('drive', 'v3', credentials=credentials)
  return service