import threading
from functions import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

download_buttons = []

#Sys Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#Frame
app = ctk.CTk()
app.title("LynTube")
app.geometry("550x350")

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

def set_buttons_state(state):
    for btn in download_buttons:
        if state == "disabled":
            btn.configure(state="disabled", fg_color="#3a3a3a", text_color="#a0a0a0")
        else:
            btn.configure(state="normal", fg_color="#1f6aa5", text_color="white")

def threaded_dwn(target_function, *args):
    def run():
        set_buttons_state("disabled")
        try:
            target_function(*args)
        finally:
            set_buttons_state("normal")
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()

def download_2160p():
    threaded_dwn(dwn_with_resolution, link_space.get(), status_text, p_bar, p_per, "2160p")
btn_2160p = ctk.CTkButton(res_frame, text="2160p", width=60, command=download_2160p)
btn_2160p.grid(row=0, column=0, padx=5)
download_buttons.append(btn_2160p) 

def download_1440p():
    threaded_dwn(dwn_with_resolution, link_space.get(), status_text, p_bar, p_per, "1440p")
btn_1440p = ctk.CTkButton(res_frame, text="1440p", width=60, command=download_1440p)
btn_1440p.grid(row=0, column=1, padx=5)
download_buttons.append(btn_1440p)  

def download_1080p():
    threaded_dwn(dwn_with_resolution, link_space.get(), status_text, p_bar, p_per, "1080p")
btn_1080p = ctk.CTkButton(res_frame, text="1080p", width=60, command=download_1080p)
btn_1080p.grid(row=0, column=2, padx=5)
download_buttons.append(btn_1080p) 

def download_720p():
    threaded_dwn(dwn_with_resolution, link_space.get(), status_text, p_bar, p_per, "720p")
btn_720p = ctk.CTkButton(res_frame, text="720p", width=60, command=download_720p)
btn_720p.grid(row=0, column=3, padx=5)
download_buttons.append(btn_720p) 

def download_480p():
    threaded_dwn(dwn_with_resolution, link_space.get(), status_text, p_bar, p_per, "480p")
btn_480p = ctk.CTkButton(res_frame, text="480p", width=60, command=download_480p)
btn_480p.grid(row=0, column=4, padx=5)
download_buttons.append(btn_480p)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

def start_download_audio():
    dwn_audio(link_space.get(), status_text, p_bar, p_per)

audio_button = ctk.CTkButton(button_frame, text="Download Audio Only", command=start_download_audio)
audio_button.grid(row=0, column=1, padx=5)
download_buttons.append(audio_button)

def open_settings():
    global current_folder
    folder = filedialog.askdirectory(title="Select Download Folder")
    if folder:
        set_download_folder(folder)
        current_folder = folder
        Folder_Text.configure(text=f"Folder set to: {folder}", text_color="#00FF00")
        app.after(2000, lambda: Folder_Text.configure(text=f"Current folder: {current_folder}", text_color="#AAAAAA"))
        
settings_button = ctk.CTkButton(app, text="⚙️", width=40, height=40, command=open_settings)
settings_button.pack(padx= 15, pady=15)
download_buttons.append(settings_button)

Folder_Text = ctk.CTkLabel(app, text="")
Folder_Text.pack()

#Config File On Startup
current_folder = get_download_folder()
if current_folder:
    Folder_Text.configure(text=f"Current folder: {current_folder}", text_color="#AAAAAA")

#App Runner
app.mainloop()