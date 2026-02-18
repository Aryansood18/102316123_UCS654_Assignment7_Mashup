# YouTube Mashup Generator

This project allows you to create a mashup of YouTube videos by a specific singer. The videos are downloaded, trimmed to a specific duration, combined into a single audio file, and can be sent directly to your email.

---

## Features

- Download multiple videos from YouTube by singer name.
- Trim each video to a specific duration.
- Combine all audio into one mashup file.
- Send the mashup as a ZIP file via email.
- Works via **CLI** or **Streamlit web app**.

---

## Requirements

- Python 3.9+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [pydub](https://pypi.org/project/pydub/)
- [streamlit](https://streamlit.io/)
- ffmpeg installed on your system
- Gmail account with **App Password** (for email feature)
- `.env` file containing:

