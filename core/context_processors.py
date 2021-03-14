from .models import Category, Post, Recurring, Tag


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
        'facebook': 'https://facebook.com/ashutoshkrris',
        'twitter': 'https://twitter.com/iReadBot',
        'instagram': 'https://instagram.com/ashutoshkrris',
        'linkedin': 'https://linkedin.com/in/ashutoshkrris',
        'portfolio': 'https://ashutoshkrris.tk'
    }
    return {'links': links}
