from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Series, Tag
from django.conf import settings

if settings.DEBUG:
    protocol = 'http'
else:
    protocol = 'https'


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = protocol

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.date_updated


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = protocol

    def items(self):
        return Category.objects.all()


class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = protocol

    def items(self):
        return Tag.objects.all()


class SeriesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = protocol

    def items(self):
        return Series.objects.all()

    def lastmod(self, obj):
        return obj.date_updated
