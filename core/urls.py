"""blog URL Configuration

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
from .views import index, about, like_dislike_post, new_post, single, contact, search, category, tag
from authentication.middlewares.auth import auth_middleware, login_excluded


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('posts/<slug>', single, name='single'),
    path('contact', contact, name='contact'),
    path('categories/<category_name>', category, name='category'),
    path('tags/<tag_name>', tag, name='tag'),
    path('search', search, name='search'),
    path('like_dislike', like_dislike_post, name='like_dislike_post'),
    path('new-post', new_post, name='new_post'),
]
