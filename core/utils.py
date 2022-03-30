import cloudinary
from django.conf import settings
import html
from django.utils.html import strip_tags
import os
from decouple import config
import requests

BASE_URL = "http://api.voicerss.org/"


def convert_to_audio(post):
    content = strip_tags(html.unescape(post.content))

    if settings.DEBUG:
        if not os.path.exists(f"{settings.MEDIA_ROOT}/blog/audio/"):
            os.mkdir(f"{settings.MEDIA_ROOT}/blog/audio/")
        filename = f"{settings.MEDIA_ROOT}/blog/audio/audio_{post.id}.wav"
    else:
        filename = f"{settings.TEMP_MEDIA_DIR}/audio_{post.id}.wav"

    params = {
        'key': config("VOICERSS_API"),
        'hl': 'en-us',
        'v': 'Mike',
        'c': 'wav',
        'f': '8khz_8bit_mono'
    }

    data = {
        'src': content,
    }

    response = requests.post(BASE_URL, data=data, params=params)

    if response.status_code == 200:
        with open(filename, "bx") as f:
            f.write(response.content)

    post.audio_url = f"{settings.MEDIA_URL}blog/audio/audio_{post.id}.wav"
    if not settings.DEBUG:
        response = upload_to_cloudinary(filename, post)
        post.audio_url = response.get('secure_url')
    post.save()


def upload_to_cloudinary(audio_file, post):
    cloudinary.config(
        cloud_name=config("CLOUD_NAME"),
        api_key=config("API_KEY"),
        api_secret=config("API_SECRET"),
        secure=True
    )
    response = cloudinary.uploader.upload(
        audio_file, public_id=f"audio_{post.id}", folder="media/blog/audio/", resource_type="video")
    os.remove(audio_file)
    return response
