
from functions.helpers.authenticate import authenticate_drive
import os
from dotenv.main import load_dotenv
import io
from googleapiclient.http import MediaIoBaseDownload

class DriveFunctions():
  def __init__(self,):
    load_dotenv()
    file_path=os.getenv('service_account_file_path')
    
    self.service=authenticate_drive(file_path=file_path)
    self.driveId=os.getenv('driveId')
  def get_image_id(self,name,folder_id):
    files=self.get_files(folder_id,driveId=self.driveId)
    return [x for x in files if x['name']==f'{name}'][0]['id']
  def get_image(self,name,folder_id):
    fileId=self.get_image_id(name,folder_id)
    request = self.service.files().get_media(fileId=fileId)
    fh = io.FileIO(name, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        _, done = downloader.next_chunk()
    return True
  
  def get_files(self,folderId,driveId=None):
    if driveId:
      corpora='drive'
      supportsAllDrives=True
      includeItemsFromAllDrives=True
    else:
      corpora=''
      supportsAllDrives=False
      includeItemsFromAllDrives=False
    page_token = None
    result=[]
    while True:
        response = self.service.files().list(q = f"'{folderId}' in parents",fields='nextPageToken, files(id, name)',
                                        supportsAllDrives=supportsAllDrives,
                                        driveId=driveId,
                                        corpora=corpora,
                                        includeItemsFromAllDrives =includeItemsFromAllDrives,pageToken=page_token).execute()
        for file in response.get('files', []):
            result.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return result

  def get_all_folder_ids(self,driveId):
    page_token = None
    result=[]
    while True:
        response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                        driveId=driveId,
                                        corpora='drive',
                                        includeItemsFromAllDrives =True,
                                        fields='nextPageToken, files(id, name)',
                                        supportsAllDrives=True, 
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            result.append({'name':file.get('name'), 'id':file.get('id')})
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return result

  #move file

  def move_file(self,file_id,folder_id):
    # Retrieve the existing parents to remove
    file = self.service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))

    # Move the file to the new folder
    file = self.service.files().update(
        fileId=file_id,
        supportsAllDrives=True,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()

  def create_folder(self,name,parentID=None):
    if parentID:
      parents=[parentID]
    else:
      parents=[]
    file_metadata = {
      'name': name,
      'parents' : parents,
      'mimeType': 'application/vnd.google-apps.folder'
      }
    file = self.service.files().create(body=file_metadata,supportsAllDrives=True,fields='id').execute()
    return file.get('id')

  def deletefile(self,fileId):
    self.service.files().delete(fileId=fileId,supportsAllDrives=True, ).execute()

  def create_folder_and_move(self,folder_name,driveFolderID,files):
    folder_name=f"{folder_name}"
    new_folder_id=self.create_folder(folder_name,driveFolderID)
    for file in files:
      self.move_file(file['id'],new_folder_id)
    return new_folder_id

  def find_file(self,name):
    return self.service.files().list(q=f"name='{name}'",fields='nextPageToken, files(id, name)').execute()
