import streamlit as st
import yt_dlp
from io import BytesIO

st.title("📥 YouTube Downloader (Video + Audio)")

# Input URL
url = st.text_input("Enter YouTube URL:")

# Download options
option = st.selectbox(
    "Choose download type:",
    ("Highest Quality Video", "Medium Quality Video", "Low Quality Video", "Audio (MP3)")
)

progress_bar = st.progress(0)
status_text = st.empty()

# Progress hook for yt-dlp
def progress_hook(d):
    if d["status"] == "downloading":
        if "downloaded_bytes" in d and "total_bytes" in d:
            percent = int(d["downloaded_bytes"] / d["total_bytes"] * 100)
            progress_bar.progress(percent)
            status_text.text(f"Downloading... {percent}%")
    elif d["status"] == "finished":
        progress_bar.progress(100)
        status_text.text("Download complete!")

if st.button("Download"):
    if not url.strip():
        st.error("Please enter a YouTube URL.")
    else:
        try:
            # Options for yt-dlp
            if option == "Audio (MP3)":
                ydl_opts = {
                    "format": "bestaudio",  # no FFmpeg conversion
                    "outtmpl": "%(title)s.%(ext)s",
                    "progress_hooks": [progress_hook],
                }
            else:
                format_map = {
                    "Highest Quality Video": "bestvideo+bestaudio/best",
                    "Medium Quality Video": "bv[height<=720]+ba/best[height<=720]",
                    "Low Quality Video": "bv[height<=360]+ba/best[height<=360]",
                }
                ydl_opts = {
                    "format": format_map[option],
                    "outtmpl": "%(title)s.%(ext)s",
                    "progress_hooks": [progress_hook],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Downloaded_File")
                ext = "webm" if option == "Audio (MP3)" else info.get("ext", "mp4")

            # Read file and provide download button
            file_path = f"{title}.{ext}"
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            st.download_button(
                label=f"Download {title}.{ext}",
                data=file_bytes,
                file_name=f"{title}.{ext}",
                mime="audio/webm" if option == "Audio (MP3)" else "video/mp4"
            )

        except Exception as e:
            st.error(f"Error: {e}")
