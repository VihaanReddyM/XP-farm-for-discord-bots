import time
import zipfile
import threading
import discord
import customtkinter
from datetime import datetime
import subprocess
from tqdm import tqdm
import requests
import os
import io
import shutil
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

if ModuleNotFoundError:
    os.system(r"BAT\install.bat")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

file_path = 'BAT\install.bat'

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title("Discord xp bot")
app.geometry("600x600")
app.grid_columnconfigure(0, weight=1)

# tab view
tab_control = customtkinter.CTkTabview(app)
tab_control.grid()

# adding tabs
# Create the first tab
Main_tab = tab_control.add("Main tab")
# Create the second tab
token_control = tab_control.add("tokens")
# Create the third tab
channel_id_tab = tab_control.add("channel_ids")

# path to the JSON files, configuring JSON files
settings_file = 'config/config.json'
with open(settings_file) as file:
    config_data = json.load(file)
    main_token = config_data['token']
    alt_token = config_data['token_1']
    intervals = config_data['intervals']
    random_channel = config_data['channel_ids']
    prefix = config_data['prefix']


def close_window():
    app.quit()


def button_callback():
    print("button clicked")


def program_stater():
    subprocess.call([r'BAT\run.bat'])


def profram_stopper():
    subprocess.Popen([r'BAT\program_stopper.bat'])


def discord_self_installer():
    def install_thread():
        credentials_path = 'config/credentials.json'
        folder_id = '1Wqb3PagnC8BWnNYpjcnDx8NNW2PMwbV_'
        destination_folder = ''

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
        drive_service = build('drive', 'v3', credentials=credentials)

        def download_file(file_id, destination_path):
            request = drive_service.files().get_media(fileId=file_id)
            with io.FileIO(destination_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

        def download_folder(folder_id, destination_folder):
            results = drive_service.files().list(q=f"'{folder_id}' in parents",
                                                 fields='files(id, name, mimeType)').execute()
            files = results.get('files', [])

            total_files = len(files)
            current_file = 0
            total_progress = 0

            app.update

            def create_progress_bar():
                progress_bar_widget = customtkinter.CTkProgressBar(Main_tab, width=200, height=10)
                progress_bar_widget.grid(row=4, column=0, padx=20, pady=20)
                return progress_bar_widget

            progress_bar = create_progress_bar()
            progress_bar.start()
            progress_bar.configure(
                mode='determinate', determinate_speed=0)

            for file in files:
                file_id = file['id']
                file_name = file['name']
                file_mime_type = file['mimeType']

                if file_mime_type == 'application/vnd.google-apps.folder':
                    subfolder_path = os.path.join(
                        destination_folder, file_name)
                    os.makedirs(subfolder_path, exist_ok=True)
                    download_folder(file_id, subfolder_path)
                else:
                    file_path = os.path.join(
                        destination_folder, file_name)
                    download_file(file_id, file_path)

                current_file += 1
                total_progress = round(current_file / 541, 4)
                print(total_progress)
                progress_bar.configure(determinate_speed=0)
                progress_bar.set(total_progress)
                app.update()  # Update the main event loop

                # Introduce a delay of 0.1 seconds between updates
                time.sleep(0.1)

            progress_bar.stop()
            progress_bar.destroy()

        download_folder(folder_id, destination_folder)

    # Start the download process in a separate thread
    threading.Thread(target=install_thread).start()


def main_token_callback():
    main_token = Main_token_enter.get()
    print("Successfully saved the Main token")
    config_data['token'] = main_token
    save_data_to_json()

    Main_token_enter.delete(0, customtkinter.END)


def alt_token_callback():
    alt_token = alt_token_enter.get()
    print("Successfully saved the alt token")
    config_data['token_1'] = alt_token
    save_data_to_json()

    alt_token_enter.delete(0, customtkinter.END)


def save_data_to_json():
    with open(settings_file, 'w') as file:
        json.dump(config_data, file)


def new_channel_id():
    global row_counter

    def save_channel_id():
        channel_id = new_channel_id_entry.get()
        if channel_id:
            config_data['channel_ids'].append(channel_id)
            save_data_to_json()
            new_channel_id_entry.delete(0, customtkinter.END)

    def remove_channel_id():
        channel_id = new_channel_id_entry.get()
        if channel_id in config_data['channel_ids']:
            config_data['channel_ids'].remove(channel_id)
            save_data_to_json()
            new_channel_id_entry.delete(0, customtkinter.END)

    def update_channel_ids_list():
        channel_ids_list.delete(0, customtkinter.END)
        for channel_id in config_data['channel_ids']:
            channel_ids_list.insert(customtkinter.END, channel_id)

    new_channel_id_entry = customtkinter.CTkEntry(channel_id_tab, placeholder_text="Enter your channel id")
    new_channel_id_entry.grid(row=0, column=row_counter, padx=20, pady=20)

    channel_id_saver = customtkinter.CTkButton(channel_id_tab, text='Save the channel id', command=save_channel_id)
    channel_id_saver.grid(row=1, column=row_counter, padx=20, pady=20)

    channel_id_entry_delete_button = customtkinter.CTkButton(channel_id_tab, text='Delete the channel id', command=remove_channel_id)
    channel_id_entry_delete_button.grid(row=2, column=row_counter, padx=20, pady=20)

    row_counter += 1
    row_counter = row_counter
    update_channel_ids_list()


# Update the channel_ids list with non-empty entries
config_data['channel_ids'] = [channel_id for channel_id in config_data['channel_ids'] if channel_id]

starter_button = customtkinter.CTkButton(Main_tab, text="Start the program", command=program_stater)
starter_button.grid(row=0, column=0, padx=20, pady=20)

exit_button = customtkinter.CTkButton(Main_tab, text="Stop the program", command=profram_stopper)
exit_button.grid(row=1, column=0, padx=20, pady=20)

discord_self_installer_button = customtkinter.CTkButton(Main_tab, text="Self installer", command=discord_self_installer)
discord_self_installer_button.grid(row=2, column=0, padx=20, pady=20)

close_button = customtkinter.CTkButton(Main_tab, text="Close", command=close_window)
close_button.grid(row=3, column=0, padx=20, pady=20)

# token control

Main_token_label = customtkinter.CTkLabel(token_control, text="Main token")
Main_token_label.grid(row=0, column=0, padx=20, pady=20)

Main_token_enter = customtkinter.CTkEntry(token_control, placeholder_text="Enter your main token")
Main_token_enter.grid(row=0, column=1, padx=20, pady=20)

Main_token_button = customtkinter.CTkButton(token_control, text="Save", command=main_token_callback)
Main_token_button.grid(row=0, column=2, padx=20, pady=20)

alt_token_label = customtkinter.CTkLabel(token_control, text="Alt token")
alt_token_label.grid(row=1, column=0, padx=20, pady=20)

alt_token_enter = customtkinter.CTkEntry(token_control, placeholder_text="Enter your alt token")
alt_token_enter.grid(row=1, column=1, padx=20, pady=20)

alt_token_button = customtkinter.CTkButton(token_control, text="Save", command=alt_token_callback)
alt_token_button.grid(row=1, column=2, padx=20, pady=20)

# channel id tab

scrollbar = customtkinter.CTkScrollbar(channel_id_tab, orientation="vertical")
scrollbar.grid(row=0, column=1, sticky="ns", rowspan=3)

channel_ids_list = customtkinter.CTkTextbox(channel_id_tab, yscrollcommand=scrollbar.set, width=40, height=10)
channel_ids_list.grid(row=0, column=0, padx=20, pady=20)

scrollbar.configure(command=channel_ids_list.yview)

add_new_channel_id_button = customtkinter.CTkButton(channel_id_tab, text="Add new channel ID", command=new_channel_id)
add_new_channel_id_button.grid(row=3, column=0, padx=20, pady=20)

row_counter = 4

app.mainloop()
