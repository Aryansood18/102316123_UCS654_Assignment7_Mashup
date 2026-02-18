import os
import sys
import shutil
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


def check_input():
    if len(sys.argv) != 5:
        print("Incorrect usage of script")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        number = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Number of videos and duration must be integers")
        sys.exit(1)

    if number <= 10:
        print("Number of videos must be greater than 10")
        sys.exit(1)

    if duration <= 20:
        print("Duration must be greater than 20 seconds")
        sys.exit(1)

    output_file = sys.argv[4]

    return singer, number, duration, output_file


singer, number, duration, output_file = check_input()

try:
    download_video(singer, number)
    process_audio(duration, output_file)
    print("Output file created successfully")
except Exception as error:
    print(f"An error occurred: {error}")
finally:
    shutil.rmtree("downloads", ignore_errors=True)
