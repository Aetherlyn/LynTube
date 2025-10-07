import os
import sys
import json
import subprocess
from pytubefix import YouTube
from pytubefix.cli import on_progress

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
def dwn_highest(url, status_label, p_bar, p_per,):
    folder = get_download_folder() or os.getcwd()
    try:
        def progress_callback(stream, chunk, bytes_remaining):
            bar_progress(stream, chunk, bytes_remaining, p_bar, p_per)

        yt = YouTube(url, on_progress_callback=progress_callback)
        

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', type='video').order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if not video_stream or not audio_stream:
            status_label.configure(text="No suitable streams found.", text_color="#FF0000")
            return

        base_name = yt.title.replace("/", "_").replace("\\", "_")
        video_path = os.path.join(folder, f"{base_name}_video.mp4")
        audio_path = os.path.join(folder, f"{base_name}_audio.mp4")
        output_path = os.path.join(folder, f"{base_name}.mp4")

        status_label.configure(text="Downloading video...", text_color="#AAAAAA")
        video_stream.download(output_path=folder, filename=f"{base_name}_video.mp4")

        status_label.configure(text="Downloading audio...", text_color="#AAAAAA")
        audio_stream.download(output_path=folder, filename=f"{base_name}_audio.mp4")

        status_label.configure(text="Merging video and audio...", text_color="#AAAAAA")
        ffmpeg_path = get_ffmpeg_path() 
        merge_cmd = [ffmpeg_path, "-y", "-i", video_path, "-i", audio_path, "-c", "copy", output_path]
      
        try:
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status_label.configure(text="Download Complete", text_color="#00FF00")
        except FileNotFoundError:
            status_label.configure(text="FFmpeg not found. Please install FFmpeg.", text_color="#FF0000")
            return

        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

    except:
        status_label.configure(text="Download Error: Invalid URL", text_color="#FF0000")
        


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