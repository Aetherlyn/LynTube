from functions import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

#Sys Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#Frame
app = ctk.CTk()
app.title("LynTube")
app.geometry("700x350")

#Link Bar
url = tk.StringVar()
link_space = ctk.CTkEntry(app, width=350, height=40, textvariable = url)
link_space.pack(padx=10, pady=10 )

#Progress Bar and Text
p_per = ctk.CTkLabel(app, text="0%")
p_per.pack()

p_bar = ctk.CTkProgressBar(app, width=300)
p_bar.set(0)
p_bar.pack(padx=10, pady=10)

# Status Label
status_text = ctk.CTkLabel(app, text="")
status_text.pack()

#Buttons
res_frame = ctk.CTkFrame(app)
res_frame.pack(pady=5)

def download_2160p():
    dwn_with_resolution(link_space.get(), status_text, p_bar, p_per, "2160p")
ctk.CTkButton(res_frame, text="2160p", width=60, command=download_2160p).grid(row=0, column=0, padx=5) 

def download_1440p():
    dwn_with_resolution(link_space.get(), status_text, p_bar, p_per, "1440p")
ctk.CTkButton(res_frame, text="1440p", width=60, command=download_1440p).grid(row=0, column=1, padx=5) 

def download_1080p():
    dwn_with_resolution(link_space.get(), status_text, p_bar, p_per, "1080p")
ctk.CTkButton(res_frame, text="1080p", width=60, command=download_1080p).grid(row=0, column=2, padx=5)

def download_720p():
    dwn_with_resolution(link_space.get(), status_text, p_bar, p_per, "720p")
ctk.CTkButton(res_frame, text="720p", width=60, command=download_720p).grid(row=0, column=3, padx=5)

def download_480p():
    dwn_with_resolution(link_space.get(), status_text, p_bar, p_per, "480p")
ctk.CTkButton(res_frame, text="480p", width=60, command=download_480p).grid(row=0, column=4, padx=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

def start_download_audio():
    dwn_audio(link_space.get(), status_text, p_bar, p_per)

Audio_Button = ctk.CTkButton(button_frame, text="Download Audio Only", command=start_download_audio)
Audio_Button.grid(row=0, column=1, padx=5)

def open_settings():
    global current_folder
    folder = filedialog.askdirectory(title="Select Download Folder")
    if folder:
        set_download_folder(folder)
        current_folder = folder
        Folder_Text.configure(text=f"Folder set to: {folder}", text_color="#00FF00")
        app.after(2000, lambda: Folder_Text.configure(text=f"Current folder: {current_folder}", text_color="#AAAAAA"))
        
Settings_Button = ctk.CTkButton(app, text="⚙️", width=40, height=40, command=open_settings)
Settings_Button.pack(pady=5)

Folder_Text = ctk.CTkLabel(app, text="")
Folder_Text.pack()

#Config File On Startup
current_folder = get_download_folder()
if current_folder:
    Folder_Text.configure(text=f"Current folder: {current_folder}", text_color="#AAAAAA")

#App Runner
app.mainloop()