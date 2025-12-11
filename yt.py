import streamlit as st
from yt_dlp import YoutubeDL
from io import BytesIO

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

    # Streamlit progress feedback
    progress_text = st.empty()
    progress_bar = st.progress(0)

    # Define yt-dlp options
    ydl_opts = {}

    if option == "Audio (MP3)":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [lambda d: progress_bar.progress(int(d.get('downloaded_bytes', 0)/d.get('total_bytes', 1)*100) if d.get('total_bytes') else 0)],
        }
    else:
        # Choose quality
        if option == "Highest Quality Video":
            fmt = 'bestvideo+bestaudio/best'
        elif option == "Medium Quality Video":
            fmt = 'bestvideo[height<=720]+bestaudio/best'
        else:
            fmt = 'bestvideo[height<=360]+bestaudio/best'

        ydl_opts = {
            'format': fmt,
            'merge_output_format': 'mp4',
            'progress_hooks': [lambda d: progress_bar.progress(int(d.get('downloaded_bytes', 0)/d.get('total_bytes', 1)*100) if d.get('total_bytes') else 0)],
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)
            ydl.download([url])

        # Read file to offer download in Streamlit
        with open(filename, "rb") as f:
            file_bytes = f.read()

        st.success("Download completed!")
        st.download_button(
            label="Click to download",
            data=file_bytes,
            file_name=filename,
            mime="video/mp4" if option != "Audio (MP3)" else "audio/mp3"
        )

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure you have ffmpeg installed (packages.txt contains ffmpeg).")
