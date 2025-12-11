import streamlit as st
import yt_dlp
import os
from pathlib import Path

# Fixed Windows-friendly Downloads folder path
download_path = str(Path.home() / "Downloads") + "\\"

st.title("📥 YouTube Downloader (Video + MP3)")

url = st.text_input("Enter YouTube URL:")

option = st.selectbox(
    "Choose download type:",
    ("Highest Quality Video", "Medium Quality Video", "Low Quality Video", "Audio (MP3)")
)

progress_bar = st.progress(0)
status_text = st.empty()

def progress_hook(d):
    if d["status"] == "downloading":
        if "downloaded_bytes" in d and "total_bytes" in d:
            percent = int(d["downloaded_bytes"] / d["total_bytes"] * 100)
            progress_bar.progress(percent)
            status_text.text(f"Downloading... {percent}%")
    elif d["status"] == "finished":
        progress_bar.progress(100)
        status_text.text("Finalizing...")

if st.button("Download"):
    if not url.strip():
        st.error("Please enter a URL.")
    else:
        try:
            if option == "Audio (MP3)":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": download_path + "%(title)s.%(ext)s",
                    "progress_hooks": [progress_hook],
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            else:
                format_map = {
                    "Highest Quality Video": "bestvideo+bestaudio/best",
                    "Medium Quality Video": "bv[height<=720]+ba/best[height<=720]",
                    "Low Quality Video": "bv[height<=360]+ba/best[height<=360]",
                }

                ydl_opts = {
                    "format": format_map[option],
                    "outtmpl": download_path + "%(title)s.%(ext)s",
                    "progress_hooks": [progress_hook],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Downloaded File")

            st.success(f"Download complete! Saved to: {download_path}")

        except Exception as e:
            st.error(f"Error: {e}")
