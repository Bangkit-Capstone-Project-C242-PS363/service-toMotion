import re
import requests
import os
import tempfile
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
from PIL import Image
import numpy
from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime


def getWords():
    words = []
    with open("words.txt", "r") as file:
        for line in file:
            words.append(line.strip())
    return words


def getLinkPhoto(data):
    if data.isdigit():
        return f"https://storage.googleapis.com/bucket-asl-data/material-quiz/numbers/{data}.jpeg"
    else:
        return f"https://storage.googleapis.com/bucket-asl-data/material-quiz/alphabets/{data}.jpeg"


def getLinkVideo(data):
    firstLetter = ord(data[0])
    path = ""
    if firstLetter % 2 == 0:
        path = f"{chr(firstLetter - 1)}-{chr(firstLetter)}"
    else:
        path = f"{chr(firstLetter)}-{chr(firstLetter + 1)}"
    return f"https://storage.googleapis.com/bucket-asl-data/material-quiz/{path.upper()}/{data}.mp4"


def download_file(url, temp_dir):
    file_name = os.path.join(temp_dir, os.path.basename(url))

    if os.path.exists(file_name):
        return file_name

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")

    with open(file_name, "wb") as f:
        f.write(response.content)
    return file_name


def create_video_from_urls(urls, output_path):
    clips = []
    target_size = (480, 320)  # Set a standard size
    fps = 30  # Set a standard frame rate

    with tempfile.TemporaryDirectory() as temp_dir:
        for url in urls:
            try:
                file_path = download_file(url, temp_dir)
                if url.endswith(".mp4"):
                    clip = VideoFileClip(file_path)
                    clip = clip.resize(target_size)
                    clip = clip.set_fps(fps)
                elif url.endswith((".jpeg", ".jpg", ".png")):
                    # Using Resampling.LANCZOS instead of ANTIALIAS
                    img = Image.open(file_path)
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    clip = ImageClip(numpy.array(img)).set_duration(2)

                if len(clips) > 0:
                    clip = clip.crossfadein(0.2)

                clips.append(clip)
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue

        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")

            final_clip.write_videofile(
                f"{output_path}.mp4",
                fps=fps,
                codec="libx264",
                bitrate="8000k",
                audio=False,
                preset="medium",
                threads=4,
            )

            for clip in clips:
                clip.close()
            final_clip.close()


def upload_with_explicit_credentials(
    bucket_name, source_file_path, destination_blob_name
):
    # Path to your service account key JSON file
    key_path = "./service-account.json"

    # Create credentials object
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create storage client with credentials
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)


def tomotion(data):
    data = data.lower()
    data = re.sub(r"[^\w\s]", "", data)
    datas = data.split()
    words = getWords()

    links = []
    for dat in datas:
        if dat in words:
            links.append(getLinkVideo(dat))
        else:
            for letter in dat:
                links.append(getLinkPhoto(letter))

    output_path = f"output/{datetime.now().strftime('%Y%m%d%H%M%S')}"
    create_video_from_urls(links, output_path)
    upload_with_explicit_credentials(
        "bucket-tomotion", f"{output_path}.mp4", f"{output_path}.mp4"
    )
    print("Uploaded")
    os.remove(f"{output_path}.mp4")
    link = f"https://storage.googleapis.com/bucket-tomotion/{output_path}.mp4"
    return link

