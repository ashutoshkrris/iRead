from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Tag


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.timestamp


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Category.objects.all()



class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Tag.objects.all()

