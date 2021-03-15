import tweepy
from decouple import config

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
    tweet = f"{post.title} by {post.author.get_full_name()} : https://iread.ga/posts/{post.slug}"
    for tag in tags:
        tweet += f" #{tag}"
    print(tweet)
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
    return link, tweet_id, full_text, retweeted