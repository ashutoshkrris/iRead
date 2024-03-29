from .models import Category, Post, Recurring, Series, Tag
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


def all_series(request):
    series = Series.objects.all().order_by('-date_updated')
    return {'all_series': series}


def recurrings(request):
    recurrings = Recurring.objects.all()
    return {'recurrings': recurrings}


def popular_posts(request):
    popular_posts = Post.objects.filter(published=True).order_by('-views')[:3]
    return {'popular_posts': popular_posts}


def recently_viewed_posts(request):
    recently_viewed_posts = Post.objects.filter(
        published=True).order_by('-date_updated')[:3]
    return {'recently_viewed_posts': recently_viewed_posts}


def social_links(request):
    links = {
        'facebook': 'https://www.facebook.com/ireadblog',
        'twitter': 'https://twitter.com/iRead_Blog',
        'instagram': 'https://instagram.com/ireadblog',
        'linkedin': 'https://linkedin.com/in/ashutoshkrris',
        'portfolio': 'https://ashutoshkrris.netlify.com',
        'dev': 'https://dev.to/ireadblog'
    }
    return {'links': links}


def latest_tweet(request):
    try:
        link, tweet_id, full_text, retweeted, date = get_latest_tweet()
        return {'connected': True, 'link': link, 'tweet_id': tweet_id, 'full_text': full_text, 'retweeted': retweeted, 'date': date}
    except Exception:
        return {'connected': False}
