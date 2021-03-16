from authentication.models import Account
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import BulletinSubscriber, Contact, Post, Category, Recurring, Tag, Comment, SubComment, Like
import random
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives, message
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from django.core.serializers import serialize
from .bot import tweet_new_post


# Create your views here.

def index(request):
    posts = Post.objects.filter(published=True).order_by('-timestamp')
    random_posts = []
    if len(posts) > 3:
        random_posts = random.sample(list(posts), 3)
    elif 0<len(posts)<=3:
        random_posts = random.choice(posts)
    if len(posts) > 8:
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
            'random_posts': random_posts,
            'pagination': True
        }
    else:
        context = {
            'posts': posts,
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
                "iRead <contact@iread.ga>",
                [email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return render(request, "core/contact.html", {'message': "We have received your details. We'll contact you soon."})
        except Exception:
            return render(request, "core/contact.html", {'error': "We are facing error this time. Please contact later."})
    return render(request, "core/contact.html")


def category(request, category_name):
    try:
        category = Category.objects.filter(name=category_name).first()
        posts = Post.objects.filter(
            published=True, categories__name=category_name)
        if len(posts) > 3:
            all_posts = Paginator(posts, 3)
            page = request.GET.get('page')
            try:
                page_posts = all_posts.page(page)
            except PageNotAnInteger:
                page_posts = all_posts.page(1)
            except EmptyPage:
                page_posts = all_posts.page(all_posts.num_pages)
            context = {
                'category': category,
                'posts': page_posts,
                'pagination': True
            }
        else:
            context = {
                'category': category,
                'posts': posts
            }
        return render(request, "core/category.html", context)
    except Exception as e:
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
            Q(categories__name__icontains=post.categories)).exclude(id=post.id).distinct()[:3]
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
            'total_likes': total_likes,
            'meta': True
        }
        return render(request, "core/blog-single.html", context)
    except Exception as e:
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
        post.likes = total_likes
        post.save()
        return JsonResponse({'is_liked': is_liked, 'total_likes': total_likes})
    except Exception:
        return JsonResponse({'like_error': 'You are not logged in.'})


def search(request):
    query = request.GET.get('query')
    results = Post.objects.filter(Q(title__icontains=query) | Q(
        seo_overview__icontains=query) | Q(content__icontains=query)).distinct()
    if len(results) > 5:
        all_posts = Paginator(results, 5)
        page = request.GET.get('page')
        try:
            page_posts = all_posts.page(page)
        except PageNotAnInteger:
            page_posts = all_posts.page(1)
        except EmptyPage:
            page_posts = all_posts.page(all_posts.num_pages)
        context = {
            'query': query,
            'results': page_posts,
            'pagination': True
        }
    else:
        context = {
            'query': query,
            'results': results
        }
    return render(request, "core/search.html", context)


def tag(request, tag_name):
    try:
        tag = Tag.objects.filter(name=tag_name).first()
        posts = Post.objects.filter(
            published=True, tags__name=tag_name)
        if len(posts) > 3:
            all_posts = Paginator(posts, 3)
            page = request.GET.get('page')
            try:
                page_posts = all_posts.page(page)
            except PageNotAnInteger:
                page_posts = all_posts.page(1)
            except EmptyPage:
                page_posts = all_posts.page(all_posts.num_pages)
            context = {
                'tag': tag,
                'posts': page_posts,
                'pagination': True
            }
        else:
            context = {
                'tag': tag,
                'posts': posts
            }
        return render(request, "core/tag.html", context)
    except Exception as e:
        return Http404()


def new_post(request):
    context = {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()
    }
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            banner = request.FILES.get('banner_image')
            overview = request.POST.get('overview')
            content = request.POST.get('editor1')
            category = request.POST.get('category')
            tags = request.POST.getlist('tags')
            published = request.POST.get('published')

            cat = Category.objects.get(name=category)
            user = Account.objects.get(id=request.session.get('user_id'))
            new_post = Post(title=title, seo_overview=overview,
                            thumbnail=banner, content=content, author=user, categories=cat, published=bool(published))
            new_post.save()
            post = Post.objects.get(title=title, author=user)
            for tag in tags:
                post.tags.add(Tag.objects.get(name=tag))
            post.save()
            if post.published:
                tweet_new_post(post, tags)
            return redirect('single', slug=post.slug)
        except ValueError:
            context['error'] = 'One or more fields is missing.'
            return render(request, "core/new-post.html", context)
    return render(request, "core/new-post.html", context)


def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    context = {
        'post': post
    }
    if request.method == 'POST':
        try:

            title = request.POST.get('title')
            try:
                banner = request.FILES['banner_image']
                post.thumbnail = banner
            except Exception:
                pass
            overview = request.POST.get('overview')
            content = request.POST.get('editor1')
            published = request.POST.get('published')
            post.title = title
            post.seo_overview = overview
            post.content = content
            post.published = bool(published)
            post.save()
            return redirect('single', slug=post.slug)
        except ValueError:
            context['error'] = 'One or more fields is missing.'
            return render(request, "core/update-post.html", context)
    return render(request, "core/update-post.html", context)


def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return redirect('home')


def new_category(request):
    if request.method == 'POST':
        if request.session.get('user_id'):
            data = json.loads(request.body)
            category_name = data['category_name']
            capitalized_category = " ".join([
                word.capitalize()
                for word in category_name.split(" ")
            ])
            if not Category.objects.filter(name=capitalized_category).exists():
                try:
                    new_category = Category(name=capitalized_category)
                    new_category.save()
                    print("Created new")
                    return JsonResponse({'category_created': 'Category created successfully.'})
                except Exception:
                    return JsonResponse({'category_error': 'Error while creating category.'})
            else:
                return JsonResponse({'category_error': 'Category already exists.'})
        else:
            return JsonResponse({'category_error': 'You are not logged in.'})
    else:
        return JsonResponse({'category_error': 'Unable to create new category'})


def new_tag(request):
    if request.method == 'POST':
        if request.session.get('user_id'):
            data = json.loads(request.body)
            tag_name = data['tag_name']
            lower_tag = "_".join([
                word.lower()
                for word in tag_name.split(" ")
            ])
            if not Tag.objects.filter(name=lower_tag).exists():
                try:
                    new_tag = Tag(name=lower_tag)
                    new_tag.save()
                    return JsonResponse({'tag_created': 'Tag created successfully.'})
                except Exception:
                    return JsonResponse({'tag_error': 'Error while creating tag.'})
            else:
                return JsonResponse({'tag_error': 'Tag already exists.'})
        else:
            return JsonResponse({'tag_error': 'You are not logged in.'})
    else:
        return JsonResponse({'tag_error': 'Unable to create new tag'})


# For bulletins registration
def bulletin_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data["name"]
        email = data['email']
        if BulletinSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'registration_duplicate': True})
        category_id = data['category']
        recurring_id = data['recurring']
        category = Category.objects.get(id=category_id)
        recurring = Recurring.objects.get(id=recurring_id)
        new_subscriber = BulletinSubscriber(
            name=name, email=email, category=category, subs_type=recurring)
        new_subscriber.save()
        return JsonResponse({'registration_success': True, 'category': category.name, 'recurring': recurring.name})
    return JsonResponse({'registration_failure': True})


def bulletin_unsubscribe(request):
    context = {
        'unsubscribe': True
    }
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        try:
            subscriber = BulletinSubscriber.objects.get(email=email)
            subscriber.delete()
            return JsonResponse({'unsubscribed': 'We hope you had great time with us.'})
        except BulletinSubscriber.DoesNotExist:
            return JsonResponse({'not_found': 'You were not subscribed to our bulletins.'})
        except Exception:
            return JsonResponse({'error': 'Something went wrong.'})
    return render(request, "core/contact.html", context)


def bulletin_email():
    subscribers = BulletinSubscriber.objects.all()
    for sub in subscribers:
        sub_type = sub.subs_type.name
        latest_posts = Post.objects.filter(
            categories__id=sub.category.id).order_by('-timestamp')[:2]
        lp1, lp2 = latest_posts[0], latest_posts[1]

        popular_posts = Post.objects.filter(
            categories__id=sub.category.id).order_by('-likes')[:2]
        pp1, pp2 = popular_posts[0], popular_posts[1]

        context = {
            'lp1': lp1,
            'lp2': lp2,
            'pp1': pp1,
            'pp2': pp2,
            'category': sub.category.name,
            'sub_type': sub_type,
            'email': sub.email
        }
        try:
            html_content = render_to_string("emails/bulletins.html", context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                f"{sub_type.capitalize()} Bulletins For You | iRead",
                text_content,
                "iRead <bulletins@iread.ga>",
                [sub.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            print(e)
            pass


def privacy_policy(request):
    return render(request, "core/important-docs/privacy-policy.html")


def terms_conditions(request):
    return render(request, "core/important-docs/tnc.html")


def refund_policy(request):
    return render(request, "core/important-docs/refund-policy.html")

# Public API to fetch all posts


def pub_api(request):
    posts = Post.objects.filter(published=True)
    data = serialize("json", posts, fields=('title', 'slug', 'timestamp',))
    return HttpResponse(data, content_type="application/json")
