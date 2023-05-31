import tkinter
import discord
import customtkinter
from datetime import datetime
import subprocess

now = datetime.now()
time = now.strftime("%H:%M:%S")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x200")
app.grid_columnconfigure(0, weight=1)


def close_window():
    app.quit()

def button_callback():
    print("button clicked")

def program_stater():
    subprocess.call([r'run.bat'])

def profram_stopper():
    subprocess.Popen([r'program_stopper.bat'])


starter_button = customtkinter.CTkButton(app, text="Start the program", command=program_stater) 
starter_button.grid(row=0, column=0, padx=20, pady=20)


stop_button = customtkinter.CTkButton(app, text="Stop the program", command=profram_stopper)
stop_button.grid(row=1, column=0, padx=20, pady=20)

exit_button = customtkinter.CTkButton(app, text="Exit this window", command=close_window)
exit_button.grid(row=2, column=0, padx=20, pady=20)


app.mainloop()
