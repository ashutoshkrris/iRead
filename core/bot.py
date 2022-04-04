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
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def tweet_new_post(post, tags):
    iread_bot = authenticate()
    try:
        author = f'@{post.author.social_links.twitter_username}'
        if not author or author == '':
            author = f'{post.author.get_full_name()}'
    except Exception:
        author = f'{post.author.get_full_name()}'
    tweet = f"'{post.title}' by {author} 😀: https://ireadblog.com{post.get_absolute_url()}"
    if type(tags) != list:
        tags = list(tags)
    tags.append("iReadBlog")
    for tag in tags:
        tweet += f" #{tag}"
    try:
        iread_bot.update_status(tweet)
        post.tweeted = True
        post.save()
    except Exception as e:
        print(e)


def tweet_series(series):
    iread_bot = authenticate()
    try:
        author = f'@{series.user.social_links.twitter_username}'
        if not author or author == '':
            author = f'{series.user.get_full_name()}'
    except Exception:
        author = f'{series.user.get_full_name()}'
    tweet = f"'{series.name}' by {author} 😀 : https://ireadblog.com{series.get_absolute_url()}"
    try:
        iread_bot.update_status(tweet)
    except Exception as e:
        print(e)


def get_latest_tweet():
    iread_bot = authenticate()
    response = iread_bot.user_timeline(
        user_id="iReadBot", count=1, tweet_mode="extended")[0]
    data = response._json
    try:
        link = data['entities']['urls'][0]['url']
    except Exception:
        link = ""
    tweet_id = data['id_str']
    full_text = data['full_text']
    retweeted = bool(data["retweeted"])
    date = data["created_at"]
    return link, tweet_id, full_text, retweeted, date

