import os
import json
from pytubefix import YouTube
from pytubefix.cli import on_progress

CONFIG_FILE = "config.json"

#Config functions
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as file:
            json.dump({"download_folder": ""}, file)
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def get_download_folder():
    config = load_config()
    return config.get("download_folder", "")

def set_download_folder(folder):
    config = load_config()
    config["download_folder"] = folder
    save_config(config)



def dwn_highest(url, status_label, p_bar, p_per):
    folder = get_download_folder() or os.getcwd()
    try:

        def progress_callback(stream, chunk, bytes_remaining):
            bar_progress(stream, chunk, bytes_remaining, p_bar, p_per)

        yt = YouTube(url, on_progress_callback=progress_callback)
        vid = yt.streams.get_highest_resolution()
        vid.download(output_path=folder)
        status_label.configure(text="Video Download Complete", text_color="#00FF00")
    except:
        status_label.configure(text=f"Download Error: Invalid URL", text_color="#FF0000")
        


def dwn_audio(url, status_label, p_bar, p_per):
    folder = get_download_folder() or os.getcwd()
    try:
        def progress_callback(stream, chunk, bytes_remaining):
            bar_progress(stream, chunk, bytes_remaining, p_bar, p_per)

        yt = YouTube(url, on_progress_callback=progress_callback)
        audio = yt.streams.get_audio_only()
        audio.download(output_path=folder)
        status_label.configure(text="Audio Download Complete", text_color="#00FF00")
    except:
        status_label.configure(text="Download Error: Invalid URL", text_color="#FF0000")


def bar_progress(stream, chunk, bytes_remaining, p_bar, p_per):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completion = bytes_downloaded / total_size * 100

    p_per.configure(text=f"{int(percentage_completion)}%")
    p_per.update()

    p_bar.set(percentage_completion / 100)
    p_bar.update()