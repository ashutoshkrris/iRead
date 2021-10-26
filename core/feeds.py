from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post
from authentication.models import Account


class LatestPostsFeed(Feed):
    title = 'iRead Blog'
    link = reverse_lazy('home')
    description = 'Latest five blogs on iRead'

    def items(self):
        return Post.objects.filter(published=True)[:5]

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


class UserPostsFeed(Feed):
    title = 'iRead Blog'
    link = reverse_lazy('home')
    description = 'Latest blogs by '

    def get_object(self, request, username):
        return Account.objects.get(username=username)

    def items(self, obj):
        return Post.objects.filter(author=obj, published=True)[:5]

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
