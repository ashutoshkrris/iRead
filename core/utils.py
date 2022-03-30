import cloudinary
from core import voicerss_tts
import base64
from django.conf import settings
import html
from django.utils.html import strip_tags
import os
from decouple import config


def convert_to_audio(post):
    if post.audio_url:
        return
    content = strip_tags(html.unescape(post.content))
    voice = voicerss_tts.speech({
        'key': config("VOICERSS_API"),
        'hl': 'en-us',
        'v': 'Mike',
        'src': content,
        'r': '0',
        'c': 'mp3',
        'f': '44khz_16bit_stereo',
        'ssml': 'false',
        'b64': 'true'
    })
    if settings.DEBUG:
        if not os.path.exists(f"{settings.MEDIA_ROOT}/blog/audio/"):
            os.mkdir(f"{settings.MEDIA_ROOT}/blog/audio/")
        filename = f"{settings.MEDIA_ROOT}/blog/audio/audio_{post.id}.wav"
    else:
        filename = f"{settings.TEMP_MEDIA_DIR}/audio_{post.id}.wav"
    with open(filename, "wb") as wav_file:
        decode_string = base64.b64decode(voice["response"])
        wav_file.write(decode_string)
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
