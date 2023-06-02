import os
import io
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from tqdm import tqdm

# Set the path to your service account credentials JSON file
credentials_path = 'config\credentials.json'

# Set the ID of the folder you want to download
folder_id = '1Wqb3PagnC8BWnNYpjcnDx8NNW2PMwbV_'

# Authenticate using the service account credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])

# Create a Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

# Download a file from Google Drive
def download_file(file_id, destination_path):
    request = drive_service.files().get_media(fileId=file_id)
    with io.FileIO(destination_path, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

# Download all files and subfolders from a Google Drive folder
def download_folder(folder_id, destination_folder):
    results = drive_service.files().list(q=f"'{folder_id}' in parents", fields='files(id, name, mimeType)').execute()
    files = results.get('files', [])

    total_files = len(files)
    current_file = 0
    pbar = tqdm(total=total_files, desc='Downloading Files')

    for file in files:
        file_id = file['id']
        file_name = file['name']
        file_mime_type = file['mimeType']

        if file_mime_type == 'application/vnd.google-apps.folder':
            # If the item is a subfolder, create a corresponding local subfolder and download its contents
            subfolder_path = os.path.join(destination_folder, file_name)
            os.makedirs(subfolder_path, exist_ok=True)
            download_folder(file_id, subfolder_path)
        else:
            # If the item is a file, download it to the destination folder
            file_path = os.path.join(destination_folder, file_name)
            download_file(file_id, file_path)
            current_file += 1
            pbar.update(1)
            pbar.set_postfix({'Progress': f'{current_file}/{total_files}'})
            print('Downloaded file:', file_path)

    pbar.close()

# Set the destination folder for downloading the Google Drive folder contents
destination_folder = './src'

# Download the Google Drive folder contents
download_folder(folder_id, destination_folder)
