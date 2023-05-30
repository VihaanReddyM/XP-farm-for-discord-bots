import discord
import customtkinter
from datetime import datetime
import subprocess


now = datetime.now()
time = now.strftime("%H:%M:%S")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()


def close_window():
    if root.winfo_exists():  # Check if the window still exists
        root.destroy()

def button_callback():
    print("button clicked")

def program_stater():
    subprocess.call([r'run.bat'])


app = customtkinter.CTk()
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="my button", command=program_stater)
button.pack(padx=20, pady=20)

exit_button = customtkinter.CTkButton(app, text="Exit", command=root.quit)
exit_button.pack(pady=20)



app.mainloop()