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
from .views import FollowNotification, PostNotification, RemoveNotification, bulletin_registration, bulletin_unsubscribe, delete_post, index, about, like_dislike_post, new_post, new_series, privacy_policy, pub_api, pub_single_post_api, pub_user_posts_api, refund_policy, send_bulletin_email, series, single, contact, search, category, tag, terms_conditions, update_post, sponsor
from authentication.middlewares.auth import auth_middleware
from .feeds import LatestPostsFeed, UserPostsFeed

urlpatterns = [
    path('', index, name='home'),
    path('about/privacy-policy', privacy_policy, name='privacy_policy'),
    path('about/terms-conditions', terms_conditions, name='terms_conditions'),
    path('about/refund-policy', refund_policy, name='refund_policy'),
    path('about', about, name='about'),
    path('sponsor', sponsor, name='sponsor'),
    path('posts/<int:post_id>/<slug>', single, name='single'),
    path('contact', contact, name='contact'),
    path('categories/<category_name>', category, name='category'),
    path('tags/<tag_name>', tag, name='tag'),
    path('series/<int:series_id>/<series_slug>', series, name='series'),
    path('new-series', auth_middleware(new_series), name='new_series'),
    path('search', search, name='search'),
    path('like_dislike', like_dislike_post, name='like_dislike_post'),
    path('new-post', auth_middleware(new_post), name='new_post'),
    path('posts/<int:post_id>/<slug>/update',
         auth_middleware(update_post), name='update_post'),
    path('posts/<int:post_id>/<slug>/delete',
         auth_middleware(delete_post), name='delete_post'),
    path('bulletins/subscribe', bulletin_registration,
         name='bulletin_registration'),
    path('bulletins/unsubscribe', bulletin_unsubscribe,
         name='bulletin_unsubscribe'),
    path('send-bulletin-email',send_bulletin_email, name='send_bulletin_email'),
    path('notification/<int:notification_id>/post/<slug>',
         PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_id>/profile/<username>',
         FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_id>/<to_user>',
         RemoveNotification.as_view(), name='notification-delete'),
    path('api/v1/posts', pub_api, name='public_api'),
    path('api/v1/<str:username>/posts', pub_user_posts_api, name='pub_user_posts_api'),
    path('api/v1/post/<int:post_id>/<str:slug>', pub_single_post_api, name='pub_single_post_api'),
    path('feed/<username>', UserPostsFeed(), name='user_post_feed'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
