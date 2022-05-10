from datetime import date
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse_lazy
from django.urls.base import reverse
from .models import Post
from authentication.models import Account


class ExtendedRSSFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super(ExtendedRSSFeed, self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        attrs['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
        attrs['xmlns:cc'] = "http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html"
        return attrs


class LatestPostsFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = 'iRead Blog'
    link = reverse_lazy('home')
    description = 'Latest ten blogs on iRead'
    feed_copyright = f'© 2021-{date.today().year} iRead. All rights reserved'
    generator = 'iRead'
    # description_template = 'core/feeds/article.html'

    # Items and Elements for each item

    def items(self):
        return Post.objects.filter(published=True)[:10]

    def item_title(self, item):
        return item.title

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_pubdate(self, item):
        return item.timestamp

    def item_categories(self, item):
        return [item.categories.name]

    def item_description(self, item):
        return item.content


class UserPostsFeed(Feed):
    feed_type = ExtendedRSSFeed
    feed_copyright = f'© 2021-{date.today().year} iRead. All rights reserved'

    def title(self, user):
        return f"Latest ten blogs written by {user.get_full_name()}"

    def description(self, user):
        return f'Latest ten blogs written by {user.get_full_name()}'

    def link(self, user):
        return reverse('profile', args=[user.username])

    def get_object(self, request, username):
        return Account.objects.get(username=username)

    def items(self, obj):
        return Post.objects.filter(author=obj, published=True)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_pubdate(self, item):
        return item.timestamp

    def item_categories(self, item):
        return [item.categories.name]
