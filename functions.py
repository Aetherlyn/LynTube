import os
import re
import sys
import json
import subprocess
from pytubefix import YouTube

CONFIG_FILE = "config.json"

#ffmpeg founder, depending on being packaged with ffmpeg or not
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        bundled_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
        if os.path.exists(bundled_path):
            return bundled_path
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, "ffmpeg.exe")
    else:
        return os.path.join(os.getcwd(), "ffmpeg.exe")

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


#Button functions
def dwn_with_resolution(url, status_label, p_bar, p_per, resolution):
    folder = get_download_folder() or os.getcwd()

    try:
        def progress_callback(stream, chunk, bytes_remaining):
            bar_progress(stream, chunk, bytes_remaining, p_bar, p_per)

        yt = YouTube(url, on_progress_callback=progress_callback)

        video_stream = yt.streams.filter(res=resolution).first()
        if not video_stream:
            status_label.configure(text="No suitable video stream found.", text_color="#FF0000")
            return

        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            status_label.configure(text="No suitable audio stream found.", text_color="#FF0000")
            return

        base_name = re.sub(r'[<>:"/\\|?*]', '', yt.title)
        video_path = os.path.join(folder, f"{base_name}_video.mp4")
        audio_path = os.path.join(folder, f"{base_name}_audio.mp4")
        output_path = os.path.join(folder, f"{base_name}.mp4")

        status_label.configure(text="Downloading video...", text_color="#AAAAAA")
        video_stream.download(output_path=folder, filename=f"{base_name}_video.mp4")

        status_label.configure(text="Downloading audio...", text_color="#AAAAAA")
        audio_stream.download(output_path=folder, filename=f"{base_name}_audio.mp4")

        if not (os.path.exists(video_path) and os.path.exists(audio_path)):
            status_label.configure(text="Error: One or both media files missing.", text_color="#FF0000")
            return

        status_label.configure(text="Merging video and audio...", text_color="#AAAAAA")
        ffmpeg_path = get_ffmpeg_path()
        merge_cmd = [
            ffmpeg_path, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            output_path
        ]

        subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        status_label.configure(text="Download Complete", text_color="#00FF00")

        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

    except Exception as e:
        status_label.configure(text=f"Download Error: {str(e)}", text_color="#FF0000")


def dwn_audio(url, status_label, p_bar, p_per):
    folder = get_download_folder() or os.getcwd()
    try:
        def progress_callback(stream, chunk, bytes_remaining):
            bar_progress(stream, chunk, bytes_remaining, p_bar, p_per)

        yt = YouTube(url, on_progress_callback=progress_callback)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(output_path=folder)
        status_label.configure(text="Audio Download Complete", text_color="#00FF00")
    except Exception as e:
        status_label.configure(text=f"Download Error: {str(e)}", text_color="#FF0000")

#Percentage functions
def format_size(bytes_amount):
    for byte in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_amount < 1024:
            return f"{bytes_amount:.2f} {byte}"
        bytes_amount /= 1024
    return f"{bytes_amount:.2f} PB"

def bar_progress(stream, chunk, bytes_remaining, p_bar, p_per):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completion = bytes_downloaded / total_size * 100

    downloaded_file = format_size(bytes_downloaded)
    total_file = format_size(total_size)

    p_per.configure(text=f"{int(percentage_completion)}% ({downloaded_file} / {total_file})")
    p_per.update()

    p_bar.set(percentage_completion / 100)
    p_bar.update()