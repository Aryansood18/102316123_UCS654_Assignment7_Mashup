import os
import yt_dlp
from pydub import AudioSegment


def download_video(singer, number_of_videos):
    os.makedirs("downloads", exist_ok=True)

    search_query = f"ytsearch{number_of_videos}:{singer}"

    options = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([search_query])


def process_audio(duration, output_file):
    final_audio = AudioSegment.empty()

    for file in os.listdir("downloads"):
        file_path = os.path.join("downloads", file)

        try:
            audio = AudioSegment.from_file(file_path)
            trimmed_audio = audio[: duration * 1000]
            final_audio += trimmed_audio
        except Exception as error:
            print(f"Error while processing {file}: {error}")

    final_audio.export(output_file, format="mp3")
