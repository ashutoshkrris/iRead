from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
import json
import re
from .models import Account, OTPModel
from core.models import Post
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.utils.decorators import method_decorator
from .middlewares.auth import login_excluded

# Create your views here.


def email_validation(request):
    data = json.loads(request.body)
    email = data['email']
    if Account.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are already registered. Please login to continue.'}, status=409)
    return JsonResponse({'email_valid': True})


def username_validation(request):
    data = json.loads(request.body)
    username = data['username']
    if Account.objects.filter(username=username).exists():
        return JsonResponse({'username_error': 'Username is already taken. Please choose another'}, status=409)
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
        html_content = render_to_string("emails/otp.html", data)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            f"One Time Password | iRead",
            text_content,
            "iRead <no-reply@iRead.tk>",
            [user_email]
        )
        print("sending email")
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("Sent")
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


def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        new_user = Account(first_name=fname, last_name=lname,
                           email=email, username=username, password=password)
        new_user.password = make_password(new_user.password)
        new_user.is_active = True
        new_user.save()
        return redirect('home')
    return render(request, "authentication/signup.html")


def check_user(email):
    return Account.objects.filter(email=email).exists()


class Login(View):
    return_url = None

    @method_decorator(login_excluded(redirect_to='home'))
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "authentication/login.html")

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
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_msg = "Password is incorrect."
        else:
            error_msg = "You are not registered yet."
        return render(request, "authentication/login.html", {'error': error_msg})


def logout(request):
    request.session.clear()
    return redirect('login')


def find_email(request):
    data = json.loads(request.body)
    email = data['email']
    if not Account.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are not registered. Please signup to continue.'}, status=404)
    return JsonResponse({'email_valid': True})


def forgot_password(request):
    if request.method == "POST":
        try:
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = Account.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, "authentication/login.html", {"message": "Password changed successfully. You can now login with your new password."})
        except Exception:
            return render(request, "authentication/reset-password.html", {"error": "Password could not be changed, please try again."})
    return render(request, "authentication/reset-password.html")


def profile(request):
    user = Account.objects.get(id=request.session.get('user_id'))
    latest_posts = Post.objects.filter(published=True, author=user)
    context = {
        'user': user,
        'latest_posts': latest_posts
    }
    return render(request, "authentication/profile.html", context)
