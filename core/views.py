from django.http.response import Http404
from django.shortcuts import render
from .models import Post, Category, Tag
import random
from django.db.models import Q


# Create your views here.

def index(request):
    posts = Post.objects.filter(published=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular_posts = posts.order_by('-views')[:3]
    try:
        random_posts = random.sample(list(posts), 2)
    except ValueError:
        random_posts = random.choice(posts)
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts,
        'random_posts': random_posts,
    }
    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


def category(request, category_name):
    try:
        category = Category.objects.filter(name=category_name).first()
        posts = Post.objects.filter(
            published=True, categories__name=category_name)
        context = {
            'category': category,
            'posts': posts
        }
        return render(request, "core/category.html", context)
    except Exception as e:
        print(e)
        return Http404()


def single(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(Q(categories__name__icontains=post.categories)).exclude(id=post.id).distinct()
        post.views += 1
        post.save()
        context = {
            'post': post,
            'related_posts': related_posts
        }
        return render(request, "core/blog-single.html", context)
    except Exception as e:
        print(e)
        raise Http404()


def search(request):
    query = request.GET.get('query')
    results = Post.objects.filter(Q(title__icontains=query) | Q(
        seo_overview__icontains=query) | Q(content__icontains=query)).distinct()
    context = {
        'results': results,
        'query': query,
    }
    return render(request, "core/search.html", context)


def tag(request, tag_name):
    try:
        tag = Tag.objects.filter(name=tag_name).first()
        posts = Post.objects.filter(
            published=True, tags__name=tag_name)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, "core/tag.html", context)
    except Exception as e:
        print(e)
        return Http404()
