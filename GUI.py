import tkinter
import zipfile
import discord
import customtkinter
from datetime import datetime
import subprocess
from tqdm import tqdm
import requests
import os
import io
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

now = datetime.now()
time = now.strftime("%H:%M:%S")


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x300")
app.grid_columnconfigure(0, weight=1)


def close_window():
    app.quit()


def button_callback():
    print("button clicked")


def program_stater():
    subprocess.call([r'BAT\run.bat'])


def profram_stopper():
    subprocess.Popen([r'BAT\program_stopper.bat'])


def discord_self_installer():
    subprocess.call([r'BAT\install.bat'])
    credentials_path = 'config/credentials.json'
    folder_id = '1Wqb3PagnC8BWnNYpjcnDx8NNW2PMwbV_'
    destination_folder = ''

    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=credentials)

    def download_file(file_id, destination_path):
        request = drive_service.files().get_media(fileId=file_id)
        with io.FileIO(destination_path, 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

    def download_folder(folder_id, destination_folder):
        results = drive_service.files().list(q=f"'{folder_id}' in parents", fields='files(id, name, mimeType)').execute()
        files = results.get('files', [])

        total_files = len(files)
        current_file = 0

        progress_bar = tqdm(total=total_files, desc='Downloading Files', unit='file', ncols=60, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

        for file in files:
            file_id = file['id']
            file_name = file['name']
            file_mime_type = file['mimeType']

            if file_mime_type == 'application/vnd.google-apps.folder':
                subfolder_path = os.path.join(destination_folder, file_name)
                os.makedirs(subfolder_path, exist_ok=True)
                download_folder(file_id, subfolder_path)
            else:
                file_path = os.path.join(destination_folder, file_name)
                download_file(file_id, file_path)
                current_file += 1
                progress_bar.update(1)

        progress_bar.close()

    download_folder(folder_id, destination_folder)

starter_button = customtkinter.CTkButton(app, text="Start the program", command=program_stater)
starter_button.grid(row=0, column=0, padx=20, pady=20)

exit_button = customtkinter.CTkButton(app, text="Exit this window", command=close_window)
exit_button.grid(row=1, column=0, padx=20, pady=20)

stop_button = customtkinter.CTkButton(app, text="Stop the program", command=profram_stopper)
stop_button.grid(row=2, column=0, padx=20, pady=20)

folder_installer = customtkinter.CTkButton(app, text="Install", command=discord_self_installer)
folder_installer.grid(row=3, column=0, padx=20, pady=20)

app.mainloop()
