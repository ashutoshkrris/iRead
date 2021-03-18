"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import change_password, check_passwords, collect_password, edit_profile, edit_profile_image, find_email, forgot_password, password_validation, signup, email_validation, username_validation, match_passwords,send_otp,check_otp, Login, logout, profile
from django.views.decorators.csrf import csrf_exempt
from .middlewares.auth import auth_middleware,login_excluded

urlpatterns = [
    path('find-email/', csrf_exempt(find_email), name='find_email'),
    path('validate-email/', csrf_exempt(email_validation), name='email_validate'),
    path('validate-username/', csrf_exempt(username_validation), name='username_validate'),
    path('validate-password/', csrf_exempt(password_validation),name='password_validate'),
    path('match-passwords/', csrf_exempt(match_passwords),name='password_match'),
    path('check-passwords/', csrf_exempt(check_passwords), name='password_check'),
    path('send-otp/', send_otp, name='send_otp'),
    path('check-otp/',check_otp, name='check_otp'),
    path("signup", signup, name="signup"),
    path("login", Login.as_view(), name="login"),
    path("logout", logout, name="logout"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('change-password/', auth_middleware(change_password), name='change_password'),
    path('profile/<username>', profile, name='profile'),
    path('profile/<username>/edit', auth_middleware(edit_profile), name='edit_profile'),
    path('profile/<username>/update-profile-image', auth_middleware(edit_profile_image), name='edit_profile_image'),
    path('collect-password', collect_password, name='collect-password')
]
