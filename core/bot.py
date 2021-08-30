import tweepy
from decouple import config
import requests
from django.conf import settings

# Keys and Tokens
CONSUMER_KEY = config("TWITTER_API_KEY")
CONSUMER_SECRET_KEY = config("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = config("TWITTER_ACCESS_TOKEN_SECRET")


# Authenticate to twitter
def authenticate():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object to invoke Twitter API methods
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    return api


def tweet_new_post(post, tags):
    iread_bot = authenticate()
    author = f'@{post.author.social_links.twitter_username}'
    if len(author) == 1:
        author = f'{post.author.get_full_name()}'
    tweet = f"'{post.title}' by {author} : https://iread.ga{post.get_absolute_url()}"
    tags.append("ireadblog")
    for tag in tags:
        tweet += f" #{tag}"
    try:
        iread_bot.update_status(tweet)
    except Exception as e:
        print(e)
        pass


def get_latest_tweet():
    iread_bot = authenticate()
    response = iread_bot.user_timeline(
        id="iReadBot", count=1, tweet_mode="extended")[0]
    data = response._json
    try:
        link = data['entities']['urls'][0]['url']
    except:
        link = ""
    tweet_id = data['id_str']
    full_text = data['full_text']
    retweeted = bool(data["retweeted"])
    date = data["created_at"]
    return link, tweet_id, full_text, retweeted, date


def create_new_dev_post(post, tags):
    url = "https://dev.to/api/articles"
    headers = {
        "api-key": config("DEV_API_KEY")
    }
    if settings.DEBUG:
        main_image = f"http://127.0.0.1:8000/static/{post.thumbnail.url}"
    else:
        main_image = post.thumbnail.url
    data = {
        "article": {
            "title": f"{post.title}",
            "published": True,
            "body_markdown": f"{post.content}",
            "tags": tags,
            "canonical_url": f"https://iread.ga{post.get_absolute_url()}",
        }
    }
    try:
        x = requests.post(url=url, headers=headers, json=data)
        print(x)
    except Exception as e:
        print(e)
