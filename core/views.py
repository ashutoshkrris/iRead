from django.http.response import Http404
from django.shortcuts import render
from .models import Post, Category, Tag


# Create your views here.

def index(request):
    posts = Post.objects.filter(published=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular_posts = posts.order_by('-views')[:3]
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts
    }
    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


def single(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        popular_posts = Post.objects.filter(published=True).order_by('-views')[:3]
        post.views += 1
        post.save()
        context = {
            'post': post,
            'categories': categories,
            'tags': tags,
            'popular_posts': popular_posts
        }
        return render(request, "core/single.html", context)
    except Exception as e:
        print(e)
        raise Http404()

def base(request):
    return render(request, "core/base.html")