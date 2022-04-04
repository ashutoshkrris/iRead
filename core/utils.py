import html
from django.utils.html import strip_tags
from decouple import config
import requests

BASE_URL = "http://api.voicerss.org/"


def convert_to_audio(post):
    intro = f'{post.title} written by {post.author.get_full_name()}\n'
    content = intro + strip_tags(html.unescape(post.content))

    params = {
        'key': config("VOICERSS_API"),
        'hl': 'en-us',
        'v': 'Mike',
        'c': 'wav',
        'f': '8khz_8bit_mono',
        'b64': True
    }

    data = {
        'src': content,
    }

    response = requests.post(BASE_URL, data=data, params=params)

    if response.status_code == 200:
        post.audio_data = response.content.decode('utf-8')
        post.save()
