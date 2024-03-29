from random import choice, randint
from django.http.response import Http404
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
import json
import re
from datetime import datetime
from .models import Account, FollowersModel, OTPModel, SocialLinks, Work
from core.models import Notification, Post, Series
import string
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.utils.decorators import method_decorator
from .middlewares.auth import login_excluded
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls.base import reverse
from authentication.utils import LocationInformation, add_subscriber
from Blog.utils import send_custom_email


UPPERCASE = list(string.ascii_uppercase)
LOWECASE = string.ascii_lowercase
NUMBER = string.digits
SYMBOLS = ['@', '#', '$', '%', '&', '_']


# Create your views here.


# exception 404 view
def error_404(request, exception):

    data = {"title": "Page Not Found"}
    return render(request, 'error/404.html', data)


# exception 500 view
def error_500(request):
    data = {"title": "Server Error"}
    return render(request, 'error/500.html', data)


def email_validation(request):
    email = request.GET.get('email').strip()
    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if Account.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are already registered. Please login to continue.'})
    if not bool(re.match(pattern, email)):
        return JsonResponse({'email_error': 'Please enter a valid email address.'})
    return JsonResponse({'email_valid': True})


def username_validation(request):
    username = request.GET.get('username').strip()
    if Account.objects.filter(username=username).exists():
        return JsonResponse({'username_error': 'Username is already taken. Please choose another'})
    if len(username) < 5:
        return JsonResponse({'username_error': 'Username must be atleast 5 characters long'})
    return JsonResponse({'username_valid': True})


def password_validation(request):
    data = json.loads(request.body)
    try:
        password1 = data['password1']
    except Exception:
        password1 = data['password']
    pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%&_])(?=\S+$).{8,20}$'
    if bool(re.match(pattern, password1)):
        return JsonResponse({'password_valid': True})
    else:
        return JsonResponse({'password_error': 'Password must be 8-20 characters long and must contain atleast one uppercase letter, one lowercase letter, one number(0-9) and one special character(@,#,$,%,&,_)'})


def check_passwords(request):
    if request.method == "POST":
        user = Account.objects.get(id=request.session.get('user_id'))
        data = json.loads(request.body)
        password = data['oldPassword']
        if check_password(password, user.password):
            return JsonResponse({'password_correct': True})
        return JsonResponse({'password_error': True})


def match_passwords(request):
    data = json.loads(request.body)
    password1 = data['password1']
    password2 = data['password2']
    if str(password1) == str(password2):
        return JsonResponse({'password_match': True})
    else:
        return JsonResponse({'password_mismatch': 'Password and Confirm Password do not match.'})


def gen_otp():
    return randint(100000, 999999)


def send_otp(request):
    user_email = request.GET['email']
    try:
        user_name = request.GET['fname']
    except Exception:
        user = Account.objects.get(email=user_email)
        user_name = user.first_name
    otp = gen_otp()     # Generate OTP
    # Save OTP in database and send email to user
    try:
        OTPModel.objects.create(user=user_email, otp=otp)
        data = {
            'receiver': user_name.capitalize(),
            'otp': otp
        }
        send_custom_email(
            receiver_email=user_email,
            subject="One Time Password",
            sender_email="no-reply@ireadblog.com",
            sender_name="iRead Blog",
            template_name="otp.html",
            **data
        )
        return JsonResponse({'otp_sent': f'An OTP has been sent to {user_email}.'})
    except Exception as e:
        print(e)
        return JsonResponse({'otp_error': 'Error while sending OTP, try again'})


def match_otp(email, otp):
    otp_from_db = OTPModel.objects.filter(user=email).last().otp
    return str(otp) == str(otp_from_db)


def check_otp(request):
    req_otp = request.GET['otp']
    req_user = request.GET['email']
    if match_otp(req_user, req_otp):
        return JsonResponse({'otp_match': True})
    else:
        return JsonResponse({'otp_mismatch': 'OTP does not match.'})


@login_excluded('home')
def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        new_user = Account(first_name=fname.strip(), last_name=lname,
                           email=email.strip(), username=username.strip(), password=password.strip())
        new_user.password = make_password(new_user.password)
        new_user.is_active = True
        new_user.save()
        user = Account.objects.get(username=username)
        try:
            FollowersModel(user=user).save()
            add_subscriber(email, fname, lname, False)
        except Exception:
            pass
        try:
            data = {
                "receiver": user.first_name,
                'edit_profile_url': 'https://ireadblog.com' + reverse('edit_profile', args=[user.username])
            }
            send_custom_email(
                receiver_email=user.email,
                subject="Welcome to iRead Blog 🎉🎉",
                sender_email="no-reply@ireadblog.com",
                sender_name="iRead Blog",
                template_name="welcome.html",
                **data
            )
        except Exception:
            pass
        return render(request, "authentication/login.html", {"message": "You can now login.", "title": "Log In"})
    return render(request, "authentication/signup.html", {"title": "Sign Up"})


def check_user(email):
    return Account.objects.filter(email=email).exists()


class Login(View):
    return_url = None

    @method_decorator(login_excluded(redirect_to='home'))
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "authentication/login.html", {"title": "Log In"})

    @method_decorator(login_excluded(redirect_to='home'))
    def post(self, request):

        email = request.POST['email']
        password = request.POST['password']
        error_msg = None
        if check_user(email):
            user = Account.objects.get(email=email)
            flag = check_password(password, user.password)
            if flag:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                user.last_login = datetime.now()
                user.save()
                send_login_alert(request, user)
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_msg = "Password is incorrect."
        else:
            error_msg = "You are not registered yet."
        return render(request, "authentication/login.html", {'error': error_msg, "title": "Log In"})


def logout(request):
    request.session.clear()
    return redirect('login')


def find_email(request):
    email = request.GET.get('email')
    if not Account.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are not registered. Please signup to continue.'})
    return JsonResponse({'email_valid': True})


def forgot_password(request):
    if request.method == "POST":
        try:
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = Account.objects.get(email=email)
            user.set_password(password)
            user.pwd_changed = True
            user.save()
            return render(request, "authentication/login.html", {"message": "Password changed successfully. You can now login with your new password.", "title": "Log In"})
        except Exception:
            return render(request, "authentication/reset-password.html", {"error": "Password could not be changed, please try again.", "title": "Reset Password"})
    return render(request, "authentication/reset-password.html", {"title": "Reset Password"})


def change_password(request):
    if request.method == 'POST':
        try:
            user = Account.objects.get(id=request.session.get('user_id'))
            password = request.POST.get('newPassword1')
            user.set_password(password)
            user.pwd_changed = True
            user.save()
            request.session.clear()
            return render(request, "authentication/login.html", {"message": "Password changed successfully. You can now login with your new password.", "title": "Log In"})
        except Exception:
            return render(request, "authentication/change-password.html", {"error": "Password could not be changed, please try again.", "title": "Change Password"})
    return render(request, "authentication/change-password.html", {"title": "Change Password"})


def profile(request, username):
    user_series = None
    followers, followings = 0, 0
    try:
        user = Account.objects.get(username=username)
    except Account.DoesNotExist:
        raise Http404()
    try:
        logged_in_user = Account.objects.get(id=request.session.get('user_id'))
    except Exception:
        pass
    is_following = []
    try:
        following_obj = FollowersModel.objects.get(user=user)
    except FollowersModel.DoesNotExist:
        FollowersModel(user=user).save()
    followers, followings = following_obj.follower.count(), following_obj.following.count()
    try:
        user_series = Series.objects.filter(user=user)
    except Series.DoesNotExist:
        pass
    if request.session.get('user_id') == user.id:
        user_posts = Post.objects.filter(author=user)
    else:
        user_posts = Post.objects.filter(published=True, author=user)
        try:
            is_following = FollowersModel.objects.get(
                user=logged_in_user, following=user)
        except Exception:
            pass
    total_posts = len(user_posts)
    if total_posts > 3:
        all_posts = Paginator(user_posts, 9)
        page = request.GET.get('page', 1)
        try:
            page_posts = all_posts.page(page)
        except PageNotAnInteger:
            page_posts = all_posts.page(1)
        except EmptyPage:
            page_posts = all_posts.page(all_posts.num_pages)
        context = {
            'user': user,
            'user_posts': page_posts,
            'user_series': user_series,
            'pagination': True,
            'total_posts': total_posts,
            'is_following': is_following,
            'followers': followers,
            'followings': followings,
            'page_range': all_posts.get_elided_page_range(number=page),
            'title': user.get_full_name()
        }
    else:
        context = {
            'user': user,
            'user_posts': user_posts,
            'user_series': user_series,
            'total_posts': total_posts,
            'is_following': is_following,
            'followers': followers,
            'followings': followings,
            'title': user.get_full_name()
        }
    return render(request, "authentication/profile.html", context)


def edit_profile(request, username):
    user = Account.objects.get(id=request.session.get('user_id'))
    if user.username == username:
        context = {
            'user': user,
            'title': user.get_full_name()
        }

        if request.method == "POST":
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            about = request.POST.get('about')
            location = request.POST.get('location')
            title = request.POST.get('title')
            institution = request.POST.get('institution')
            education = request.POST.get('education')
            facebook = request.POST.get('facebook')
            youtube = request.POST.get('youtube')
            instagram = request.POST.get('instagram')
            dribble = request.POST.get('dribble')
            github = request.POST.get('github')
            gitlab = request.POST.get('gitlab')
            medium = request.POST.get('medium')
            twitter = request.POST.get('twitter')
            linkedin = request.POST.get('linkedin')
            portfolio = request.POST.get('portfolio')
            coffee = request.POST.get('coffee')
            user.first_name = fname
            user.last_name = lname
            user.about = about
            user.location = location
            if user.work:
                user.work.employer_title = title
                user.work.employer_name = institution
                user.work.education = education
            else:
                new_work = Work(employer_title=title,
                                employer_name=institution, education=education)
                new_work.save()
                user.work = new_work
            if user.social_links:
                user.social_links.youtube_url = youtube
                user.social_links.facebook_url = facebook
                user.social_links.dribble_url = dribble
                user.social_links.instagram_url = instagram
                user.social_links.github_url = github
                user.social_links.gitlab_url = gitlab
                user.social_links.medium_url = medium
                user.social_links.twitter_username = twitter
                user.social_links.linkedin_url = linkedin
                user.social_links.portfolio_url = portfolio
                user.social_links.buymeacoffee_url = coffee
            else:
                new_social = SocialLinks(youtube_url=youtube, facebook_url=facebook, dribble_url=dribble, instagram_url=instagram, github_url=github,
                                         gitlab_url=gitlab, medium_url=medium, twitter_username=twitter, linkedin_url=linkedin, portfolio_url=portfolio, buymeacoffee_url=coffee)
                new_social.save()
                user.social_links = new_social
            user.work.save()
            user.social_links.save()
            user.save()
            return redirect('profile', username=user.username)
        return render(request, 'authentication/edit_profile.html', context)
    else:
        raise Http404()


def edit_profile_image(request, username):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        try:
            user = Account.objects.get(username=username)
            user.profile_image = profile_image
            user.save()
            return JsonResponse({'image_updated': 'Profile Image changed successfully.'})
        except Exception:
            return JsonResponse({'image_error': 'Could not upload image.'})


def collect_password(request):
    data = list(UPPERCASE) + list(LOWECASE) + list(NUMBER) + SYMBOLS
    password = ''.join(choice(data) for _ in range(12))
    request.session['local_password'] = password
    return redirect(reverse('social:complete', args=('google-oauth2',)))


def send_message(request, username):
    if request.method == 'POST':
        if request.session.get('user_id'):
            sender = Account.objects.get(id=request.session.get('user_id'))
            data = json.loads(request.body)
            message = data["message"]
            receiver = Account.objects.get(username=username)
            context = {
                "sender": sender.get_full_name(),
                "receiver": receiver.first_name,
                "sender_email": sender.email,
                "message": message
            }
            try:
                send_custom_email(
                    receiver_email=receiver.email,
                    subject=f"New Message Received from {sender.get_full_name()}",
                    sender_email="no-reply@ireadblog.com",
                    sender_name="iRead Blog",
                    template_name="message.html",
                    **context
                )
                return JsonResponse({'message_success': 'Message sent successfully.'})
            except Exception:
                return JsonResponse({'message_error': 'Something went wrong.'})
        else:
            return JsonResponse({'message_error': 'You are not logged in.'})
    else:
        return JsonResponse({'message_error': 'Unable to send new message'})


def follow_user(request, username):
    logged_user = Account.objects.get(id=request.session.get('user_id'))
    try:
        to_follow = Account.objects.get(username=username)
    except Exception:
        return Http404()

    following_rel = FollowersModel.objects.filter(
        user=logged_user, following=to_follow)
    is_following = True if following_rel else False

    if is_following:
        FollowersModel.unfollow(logged_user, to_follow)
        is_following = False
    else:
        FollowersModel.follow(logged_user, to_follow)
        is_following = True
        Notification(
            notification_type=3, to_user=to_follow, from_user=logged_user).save()

    return JsonResponse({'is_following': is_following})


def stats(request, username):
    try:
        user = Account.objects.get(id=request.session.get('user_id'))
        if not user.username == username:
            raise Http404()
        user_posts = Post.objects.filter(author=user)
        sorting = request.GET.get('sort_by')
        if sorting == 'likes':
            user_posts = user_posts.order_by('-likes')
        elif sorting == 'comments':
            user_posts = user_posts.order_by('-comments')
        elif sorting == 'views':
            user_posts = user_posts.order_by('-views')
        total_views, total_likes, total_comments, total_posts, total_published_posts = 0, 0, 0, 0, 0
        for post in user_posts:
            total_views += post.views
            total_likes += post.likes
            total_comments += post.comments
            total_posts += 1
            total_published_posts += 1 if post.published else 0

        context = {
            'posts': user_posts,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_posts': total_posts,
            'total_published_posts': total_published_posts
        }
        return render(request, 'authentication/stats.html', context)
    except Account.DoesNotExist:
        raise Http404()


def send_login_alert(request, user):
    context = {
        'name': user.first_name,
        'location_data': LocationInformation.get_location(request),
        'current_time': datetime.now()
    }
    send_custom_email(
        receiver_email=user.email,
        subject=f"New login to your iRead Blog Account",
        sender_email="no-reply@ireadblog.com",
        sender_name="iRead Blog",
        template_name="login_alert.html",
        **context
    )

def delete_account(request, username):
    user = Account.objects.get(username=username)
    user.delete()
    request.session.clear()
    return redirect('login')
