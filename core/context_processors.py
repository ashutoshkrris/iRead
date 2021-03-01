from .models import Category, Post


def latest_posts(request):
    latest_posts = Post.objects.filter(
        published=True).order_by('-timestamp')[:3]
    return {'latest_posts': latest_posts}


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
