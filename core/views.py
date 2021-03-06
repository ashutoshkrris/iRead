from authentication.models import Account
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Contact, Post, Category, Tag, Comment, SubComment, Like
import random
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives, message
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def index(request):
    posts = Post.objects.filter(published=True).order_by('-timestamp')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular_posts = posts.order_by('-views')[:3]
    try:
        random_posts = random.sample(list(posts), 2)
    except ValueError:
        random_posts = random.choice(posts)

    all_posts = Paginator(posts, 8)
    page = request.GET.get('page')
    try:
        page_posts = all_posts.page(page)
    except PageNotAnInteger:
        page_posts = all_posts.page(1)
    except EmptyPage:
        page_posts = all_posts.page(all_posts.num_pages)
    context = {
        'posts': page_posts,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts,
        'random_posts': random_posts,
    }
    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        new_contact = Contact(name=name, email=email,
                              subject=subject, message=message)
        new_contact.save()
        try:
            context = {
                "name": name.split(" ")[0].capitalize()
            }
            html_content = render_to_string("emails/email.html", context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                f"Thanks for contacting iRead",
                text_content,
                "iRead <no-reply@iread.tk>",
                [email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            print(e)
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
    posts = Post.objects.filter(published=True)
    liked = []
    try:
        user = Account.objects.get(id=request.session.get('user_id'))
        
        liked = [post for post in posts if Like.objects.filter(
            post=post, user=user)]
    except Exception:
        pass
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(
            Q(categories__name__icontains=post.categories)).exclude(id=post.id).distinct()
        post.views += 1
        post.save()
        if request.method == 'POST':
            comm = request.POST.get('comm')
            comm_id = request.POST.get('comm_id')
            user = Account.objects.get(id=request.session.get('user_id'))
            if comm_id:
                SubComment(post=post,
                           user=user,
                           message=comm,
                           comment=Comment.objects.get(id=int(comm_id))
                           ).save()
            else:
                Comment(post=post, user=user, message=comm).save()
                post.comments += 1
                post.save()
        comments = []
        for comment in Comment.objects.filter(post=post):
            comments.append(
                [comment, SubComment.objects.filter(comment=comment)])
        try:
            like_obj = Like.objects.get(post=post)
            total_likes = like_obj.user.count()
        except Exception:
            total_likes = 0
        context = {
            'post': post,
            'related_posts': related_posts,
            'comments': comments,
            'liked_posts': liked,
            'total_likes': total_likes
        }
        return render(request, "core/blog-single.html", context)
    except Exception as e:
        print(e)
        raise Http404()


def like_dislike_post(request):
    post = Post.objects.get(id=request.GET.get('id'))
    try:
        user = Account.objects.get(id=request.session.get('user_id'))
        is_liked = False
        if Like.objects.filter(user=user, post=post).exists():
            Like.dislike(user=user, post=post)
        else:
            Like.like(user=user, post=post)
            is_liked = True

        like_obj = Like.objects.get(post=post)
        total_likes = like_obj.user.count()
        return JsonResponse({'is_liked': is_liked, 'total_likes': total_likes})
    except Exception:
        return JsonResponse({'like_error': 'You are not logged in.'})

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
