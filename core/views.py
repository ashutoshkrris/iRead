from django.core.files import File
from django.conf import settings
import requests
import urllib.parse
from django.db.models.functions import Concat
from django.db.models import Value as V
from datetime import datetime, date
from Blog.utils import send_custom_email
from authentication.models import Account
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import BulletinSubscriber, Contact, Notification, Post, Category, Recurring, Series, Tag, Comment, SubComment, Like
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from django.core.serializers import serialize
from .bot import tweet_new_post
from django.views import View
from urllib.parse import urlparse

# Create your views here.


def index(request):
    posts = Post.objects.filter(published=True).order_by('-timestamp')
    most_viewed = Post.objects.filter(published=True).order_by('-views')[:3]
    if len(posts) > 8:
        all_posts = Paginator(posts, 16)
        page = request.GET.get('page', 1)
        try:
            page_posts = all_posts.page(page)
        except PageNotAnInteger:
            page_posts = all_posts.page(1)
        except EmptyPage:
            page_posts = all_posts.page(all_posts.num_pages)
        context = {
            'posts': page_posts,
            'most_viewed_posts': most_viewed,
            'pagination': True,
            'page_range': all_posts.get_elided_page_range(number=page),
            'title': 'Home'
        }
    else:
        context = {
            'posts': posts,
            'most_viewed_posts': most_viewed,
            'title': 'Home'
        }

    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html", {"title": "About"})


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
            send_custom_email(
                receiver_email=email,
                subject=f"Thanks for contacting iRead Blog!",
                sender_email="contact@ireadblog.com",
                sender_name="iRead Blog",
                template_name="email.html",
                **context
            )
            return render(request, "core/contact.html", {'message': "We have received your details. We'll contact you soon.", "title": "Contact Us"})
        except Exception:
            return render(request, "core/contact.html", {'error': "We are facing error this time. Please contact later.", "title": "Contact Us"})
    return render(request, "core/contact.html", {"title": "Contact Us"})


def category(request, category_name):
    try:
        category = Category.objects.filter(name=category_name).first()
        posts = Post.objects.filter(
            published=True, categories__name=category_name)
        if len(posts) > 3:
            all_posts = Paginator(posts, 8)
            page = request.GET.get('page', 1)
            try:
                page_posts = all_posts.page(page)
            except PageNotAnInteger:
                page_posts = all_posts.page(1)
            except EmptyPage:
                page_posts = all_posts.page(all_posts.num_pages)
            context = {
                'category': category,
                'posts': page_posts,
                'pagination': True,
                'page_range': all_posts.get_elided_page_range(number=page),
                'title': category.name
            }
        else:
            context = {
                'category': category,
                'posts': posts,
                'title': category.name
            }
        return render(request, "core/category.html", context)
    except Exception as e:
        return Http404()


def series(request, series_id, series_slug):
    try:
        series = Series.objects.filter(id=series_id, slug=series_slug).first()
        posts = series.posts.all()
        if len(posts) > 3:
            all_posts = Paginator(posts, 8)
            page = request.GET.get('page', 1)
            try:
                page_posts = all_posts.page(page)
            except PageNotAnInteger:
                page_posts = all_posts.page(1)
            except EmptyPage:
                page_posts = all_posts.page(all_posts.num_pages)
            context = {
                'series': series,
                'posts': page_posts,
                'pagination': True,
                'meta_series': True,
                'page_range': all_posts.get_elided_page_range(number=page),
                'title': series.name
            }
        else:
            context = {
                'series': series,
                'posts': posts,
                'meta_series': True,
                'title': series.name
            }
        return render(request, "core/series.html", context)
    except Exception as e:
        return Http404()


def single(request, post_id, slug):
    posts = Post.objects.filter(published=True)
    series = None
    try:
        series = Series.objects.filter(posts__id=post_id).first()
    except Exception:
        pass
    liked = []
    try:
        user = Account.objects.get(id=request.session.get('user_id'))

        liked = [post for post in posts if Like.objects.filter(
            post=post, user=user)]
    except Exception:
        pass
    try:
        post = Post.objects.get(id=post_id, slug=slug)
        if not post.published and post.author.id != request.session.get('user_id'):
            raise Http404()
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
                comment = Comment.objects.get(id=comm_id)
                Notification(
                    notification_type=2, to_user=comment.user, from_user=user, post=post).save()
            else:
                Comment(post=post, user=user, message=comm).save()
                Notification(
                    notification_type=2, to_user=post.author, from_user=user, post=post).save()
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

        arr = []
        for t in post.tags.all():
            arr.append(t.name)
        tags_text = ','.join(arr)
        context = {
            'post': post,
            'meta_keywords': tags_text,
            'series': series,
            'related_posts': related_posts,
            'comments': comments,
            'liked_posts': liked,
            'total_likes': total_likes,
            'meta_post': True
        }
        if post.canonical_url:
            post_original_url = urlparse(post.canonical_url).netloc
            context['post_original_url'] = post_original_url
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
            Notification(
                notification_type=1, to_user=post.author, from_user=user, post=post).save()

        like_obj = Like.objects.get(post=post)
        total_likes = like_obj.user.count()
        post.likes = total_likes
        post.save()
        return JsonResponse({'is_liked': is_liked, 'total_likes': total_likes})
    except Exception:
        return JsonResponse({'like_error': 'You are not logged in.'})


def search(request):
    query = request.GET.get('query')
    if 'signup' in query or 'sign up' in query or 'register' in query:
        return redirect('signup')
    if 'login' in query or 'log in' in query or 'signin' in query or 'sign in' in query:
        return redirect('login')
    users = Account.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(
        Q(full_name__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    categories = Category.objects.filter(Q(name__icontains=query)).distinct()
    tags = Tag.objects.filter(Q(name__icontains=query)).distinct()
    series = Series.objects.filter(Q(name__icontains=query)).distinct()
    results = Post.objects.filter(Q(title__icontains=query) | Q(
        seo_overview__icontains=query) | Q(content__icontains=query)).distinct()
    if len(results) > 3:
        all_posts = Paginator(results, 5)
        page = request.GET.get('page', 1)
        try:
            page_posts = all_posts.page(page)
        except PageNotAnInteger:
            page_posts = all_posts.page(1)
        except EmptyPage:
            page_posts = all_posts.page(all_posts.num_pages)
        context = {
            'query': query,
            'results': page_posts,
            'pagination': True,
            'users': users[:3],
            'categories_res': categories,
            'tags': tags,
            'series': series,
            'page_range': all_posts.get_elided_page_range(number=page),
            'title': query
        }
    else:
        context = {
            'query': query,
            'results': results,
            'users': users[:3],
            'categories_res': categories,
            'tags': tags,
            'series': series,
            'title': query
        }
    return render(request, "core/search.html", context)


def tag(request, tag_name):
    try:
        tag = Tag.objects.filter(name=tag_name).first()
        posts = Post.objects.filter(
            published=True, tags__name=tag_name)
        if len(posts) > 3:
            all_posts = Paginator(posts, 8)
            page = request.GET.get('page', 1)
            try:
                page_posts = all_posts.page(page)
            except PageNotAnInteger:
                page_posts = all_posts.page(1)
            except EmptyPage:
                page_posts = all_posts.page(all_posts.num_pages)
            context = {
                'tag': tag,
                'posts': page_posts,
                'pagination': True,
                'page_range': all_posts.get_elided_page_range(number=page),
                'title': tag.name
            }
        else:
            context = {
                'tag': tag,
                'posts': posts,
                'title': tag.name
            }
        return render(request, "core/tag.html", context)
    except Exception as e:
        return Http404()


def download_blog_banner(title, user, date):
    icon_url = 'https://i.imgur.com/prMWfoZ.png'
    title = urllib.parse.quote(title)
    author = urllib.parse.quote_plus(user.get_full_name())
    icon_url = urllib.parse.quote_plus(icon_url)
    font_size = 150 if len(title) <= 40 else 125
    try:
        github_url = user.social_links.github_url
        github_username = github_url.split(".com/")[1].strip("/")
    except Exception:
        github_username = None
    if github_username:
        image_url = f"https://banners-adrianub.vercel.app/{title}.png?type=banner&theme=light&author={author}&username={github_username}&date={date}&logo={icon_url}&pattern=pixelDots&md=1&showWatermark=0&fontSize={font_size}px"
    else:
        image_url = f"https://banners-adrianub.vercel.app/{title}.png?type=banner&theme=light&author={author}&date={date}&logo={icon_url}&pattern=pixelDots&md=1&showWatermark=0&fontSize={font_size}px"
    img_data = requests.get(image_url).content
    with open(f'{settings.TEMP_MEDIA_DIR}/temp.png', 'wb') as handler:
        handler.write(img_data)


def new_post(request):
    context = {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'series': Series.objects.filter(user__id=request.session.get('user_id')),
        'title': 'Create New Post'
    }
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            banner = request.FILES.get('banner_image')
            overview = request.POST.get('overview')
            canonical_url = request.POST.get('canonical_url')
            content = request.POST.get('editor1')
            category = request.POST.get('category')
            tags = request.POST.getlist('tags')
            published = request.POST.get('published')
            series_id = request.POST.get('series')
            try:
                cat = Category.objects.get(name=category)
            except Category.DoesNotExist:
                capitalized_category = " ".join([
                    word.capitalize()
                    for word in category.split(" ")
                ])
                cat = Category(name=capitalized_category)
                cat.save()
            user = Account.objects.get(id=request.session.get('user_id'))

            if len(content.strip()) > 63:
                new_post = Post(title=title, seo_overview=overview, canonical_url=canonical_url,
                                content=content, author=user, categories=cat, published=bool(published))
                if not banner:
                    download_blog_banner(
                        title, user, date.today().strftime("%B %d, %Y"))
                    new_post.thumbnail.save(f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png", File(
                        open(f'{settings.TEMP_MEDIA_DIR}/temp.png', 'rb')))
                else:
                    new_post.thumbnail = banner
                new_post.save()
            else:
                context['error'] = 'Please enter at least 64 characters in the post content.'
                return render(request, "core/new-post.html", context)
            if(series_id):
                series = Series.objects.get(id=series_id)
                series.posts.add(new_post)
            post = Post.objects.get(title=title, author=user)
            for tag in tags:
                try:
                    post.tags.add(Tag.objects.get(name=tag))
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                    post.tags.add(new_tag)
            post.save()
            if post.published and not settings.DEBUG:
                tweet_new_post(post, tags)
            return redirect('single', post_id=post.id, slug=post.slug)
        except ValueError:
            context['error'] = 'One or more fields is missing.'
            return render(request, "core/new-post.html", context)
    return render(request, "core/new-post.html", context)


def update_post(request, post_id, slug):
    post = Post.objects.get(id=post_id, slug=slug)
    series = None
    try:
        selected_series = Series.objects.filter(posts__id=post_id).first()
    except Exception:
        pass
    context = {
        'post': post,
        'title': post.title,
        'series': Series.objects.filter(user__id=request.session.get('user_id')),
        'selected_series': selected_series.id
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
            canonical_url = request.POST.get('canonical_url')
            content = request.POST.get('editor1')
            category = request.POST.get('category')
            tags = request.POST.getlist('tags')
            published = request.POST.get('published')
            series_id = request.POST.get('series')
            post.title = title
            post.seo_overview = overview
            post.canonical_url = canonical_url
            post.content = content
            post.published = bool(published)
            post.date_updated = datetime.now()

            # Change category
            try:
                cat = Category.objects.get(name=category)
            except Category.DoesNotExist:
                capitalized_category = " ".join([
                    word.capitalize()
                    for word in category.split(" ")
                ])
                cat = Category(name=capitalized_category)
                cat.save()
            post.categories = cat

            # Change Tags
            post.tags.clear()
            for tag in tags:
                try:
                    post.tags.add(Tag.objects.get(name=tag))
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                    post.tags.add(new_tag)

            # Change series
            if(series_id):
                if selected_series:
                    selected_series.posts.remove(post)
                series = Series.objects.get(id=series_id)
                series.posts.add(post)

            post.save()
            if post.published and not post.tweeted and not settings.DEBUG:
                tweet_new_post(post, post.tags.all())
            return redirect('single', post_id=post.id,  slug=post.slug)
        except ValueError:
            context['error'] = 'One or more fields is missing.'
            return render(request, "core/update-post.html", context)
    return render(request, "core/update-post.html", context)


def delete_post(request, post_id, slug):
    post = Post.objects.get(id=post_id, slug=slug)
    post.delete()
    return redirect('home')


def new_series(request):
    if request.method == 'POST':
        if request.session.get('user_id'):
            series_name = request.POST.get('series_name')
            series_desc = request.POST.get('series_desc')
            thumbnail = request.FILES.get('thumbnail')
            print(thumbnail)
            capitalized_series = " ".join([
                word.capitalize()
                for word in series_name.split(" ")
            ])
            if not Series.objects.filter(name=capitalized_series).exists():
                try:
                    new_series = Series(
                        name=capitalized_series, desc=series_desc, thumbnail=thumbnail, user=Account.objects.get(id=request.session.get('user_id')))
                    new_series.save()
                    return redirect('series', series_id=new_series.id, series_slug=new_series.slug)
                except Exception as e:
                    print(e)
                    return render(request, 'core/new-series.html', {'error': 'Error while creating series.', 'title': 'Create New Series'})
            else:
                return render(request, 'core/new-series.html', {'error': 'Series already exists.', 'title': 'Create New Series'})
        else:
            return render(request, 'core/new-series.html', {'error': 'You are not logged in.', 'title': 'Create New Series'})
    else:
        return render(request, 'core/new-series.html', {'title': 'Create New Series'})


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


def privacy_policy(request):
    return render(request, "core/important-docs/privacy-policy.html", {"title": "Privacy Policy"})


def terms_conditions(request):
    return render(request, "core/important-docs/tnc.html", {"title": "Terms and Conditions"})


def refund_policy(request):
    return render(request, "core/important-docs/refund-policy.html", {"title": "Refund Policy"})

# Public API to fetch all posts


def pub_api(request):
    posts = Post.objects.filter(published=True)
    data = serialize("json", posts, fields=(
        'title', 'slug', 'thumbnail', 'seo_overview', 'content', 'timestamp',))
    return HttpResponse(data, content_type="application/json")


def pub_user_posts_api(request, username):
    posts = Post.objects.filter(author__username=username, published=True)
    data = serialize("json", posts, fields=(
        'title', 'slug', 'thumbnail', 'seo_overview', 'content', 'timestamp',))
    return HttpResponse(data, content_type="application/json")


def pub_single_post_api(request, post_id, slug):
    post = Post.objects.filter(id=post_id, slug=slug, published=True)
    data = serialize("json", post, fields=(
        'title', 'slug', 'thumbnail', 'seo_overview', 'content', 'timestamp',))
    return HttpResponse(data, content_type="application/json")


TODAY_DATE = datetime.today().day
TODAY_DAY = datetime.now().strftime("%A")


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

        html_content = render_to_string("emails/bulletins.html", context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            f"{sub_type.capitalize()} Bulletins For You | iRead",
            text_content,
            "iRead <bulletins@ireadblog.com>",
            [sub.email]
        )
        email.attach_alternative(html_content, "text/html")
        if (sub_type == 'Weekly' and TODAY_DAY == 'Monday'):
            email.send()
        if (sub_type == 'Monthly' and TODAY_DATE == 1):
            email.send()
        if sub_type == 'Daily':
            email.send()


def send_bulletin_email(request):
    try:
        bulletin_email()
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False})


class PostNotification(View):
    def get(self, request, notification_id, slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        post = Post.objects.get(slug=slug)

        notification.user_has_seen = True
        notification.save()

        return redirect('single', post_id=post.id, slug=slug)


class FollowNotification(View):
    def get(self, request, notification_id, username, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        profile = Account.objects.get(username=username)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', username=username)


class RemoveNotification(View):
    def delete(self, request, notification_id, to_user, *args, **kwargs):
        try:
            # to_user = Account.objects.get(id=to_user_id)
            notification = Notification.objects.get(id=notification_id)

            notification.user_has_seen = True
            notification.save()
            all_noti = Notification.objects.filter(
                to_user__email=to_user, user_has_seen=False)
            return JsonResponse({'success': True, 'noti_count': len(all_noti)})
        except Exception as e:
            print(e)
            return JsonResponse({'error': True})


def robots(request):
    return render(request, 'core/important-docs/robots.txt', content_type='text/plain')


def sponsor(request):
    return render(request, "core/sponsor.html")
