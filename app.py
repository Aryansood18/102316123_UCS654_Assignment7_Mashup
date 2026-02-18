import streamlit as st
import os
import re
import shutil
import zipfile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from helper import download_video, process_audio

load_dotenv()


def send_mail(receiver_email, zip_path):
    sender_email = "aash18ish@gmail.com"
    sender_password = os.getenv("APP_PASSWORD")

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your Mashup File"
    message.set_content("Here is your mashup file.")

    with open(zip_path, "rb") as file:
        file_data = file.read()
        file_name = os.path.basename(zip_path)

    message.add_attachment(
        file_data,
        maintype="application",
        subtype="zip",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


st.title("YouTube Mashup Generator")

singer = st.text_input("Singer Name")
num_videos = st.number_input("Number of Videos", min_value=1, step=1)
duration = st.number_input("Duration of Each Video (seconds)", min_value=2, step=1)
email = st.text_input("Email ID")

if st.button("Submit"):
    if not singer:
        st.error("Singer name is required")
    elif not is_valid_email(email):
        st.error("Invalid email address")
    else:
        try:
            os.makedirs("downloads", exist_ok=True)

            download_video(singer, int(num_videos))

            output_mp3 = "mashup.mp3"
            process_audio(int(duration), output_mp3)

            zip_file = "mashup.zip"
            with zipfile.ZipFile(zip_file, "w") as zipf:
                zipf.write(output_mp3)

            send_mail(email, zip_file)

            st.success("Mashup created and sent to your email")

        except Exception as error:
            st.error(f"Something went wrong: {error}")

        finally:
            shutil.rmtree("downloads", ignore_errors=True)

            if os.path.exists("mashup.mp3"):
                os.remove("mashup.mp3")

            if os.path.exists("mashup.zip"):
                os.remove("mashup.zip")
