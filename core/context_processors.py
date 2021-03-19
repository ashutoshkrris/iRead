from .models import Category, Post, Recurring, Tag
from .bot import get_latest_tweet


def latest_posts(request):
    latest_posts = Post.objects.filter(
        published=True).order_by('-timestamp')[:3]
    return {'latest_posts': latest_posts}


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}


def recurrings(request):
    recurrings = Recurring.objects.all()
    return {'recurrings': recurrings}


def popular_posts(request):
    popular_posts = Post.objects.filter(published=True).order_by('-likes')[:3]
    return {'popular_posts': popular_posts}


def social_links(request):
    links = {
        'facebook': 'https://www.facebook.com/ireadblog',
        'twitter': 'https://twitter.com/iReadBot',
        'instagram': 'https://instagram.com/ireadblog',
        'linkedin': 'https://linkedin.com/in/ashutoshkrris',
        'portfolio': 'https://ashutoshkrris.tk'
    }
    return {'links': links}


def latest_tweet(request):
    link, tweet_id, full_text, retweeted = get_latest_tweet()
    return {'link': link, 'tweet_id': tweet_id, 'full_text': full_text, 'retweeted': retweeted}