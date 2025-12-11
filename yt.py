import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("📥 YouTube Downloader (Video + Audio)")

# Input URL
url = st.text_input("Enter YouTube URL:")

# Download options
option = st.selectbox(
    "Choose download type:",
    ("Highest Quality Video", "Medium Quality Video", "Low Quality Video", "Audio (MP3)")
)

download_button = st.button("Download")

if download_button and url:
    
    progress_bar = st.progress(0)
    progress_text = st.empty()

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                progress_bar.progress(int(downloaded_bytes / total_bytes * 100))
        elif d['status'] == 'finished':
            progress_bar.progress(100)

    try:
        # yt-dlp options
        if option == "Audio (MP3)":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'progress_hooks': [progress_hook],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
                }
            }
        else:
            # Quality selection
            if option == "Highest Quality Video":
                fmt = 'bestvideo+bestaudio/best'
            elif option == "Medium Quality Video":
                fmt = 'bestvideo[height<=720]+bestaudio/best'
            else:
                fmt = 'bestvideo[height<=360]+bestaudio/best'

            ydl_opts = {
                'format': fmt,
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'progress_hooks': [progress_hook],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
                }
            }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([url])

        # Offer download in Streamlit
        with open(filename, "rb") as f:
            file_bytes = f.read()

        st.success("Download completed!")
        st.download_button(
            label="Click to download",
            data=file_bytes,
            file_name=filename,
            mime="audio/mp3" if option == "Audio (MP3)" else "video/mp4"
        )

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure ffmpeg is installed (packages.txt contains ffmpeg) and the video is available publicly.")
