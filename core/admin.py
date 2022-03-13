from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from core.bot import tweet_new_post, tweet_series
from .models import BulletinSubscriber, Category, Like, Notification, Recurring, Series, Tag, Post, Comment, SubComment, Contact


# Register your models here.
@admin.action(description="Toggle the published status of posts")
def toggle_published(modeladmin, request, queryset):
    for obj in queryset:
        if obj.published:
            obj.published = False
        else:
            obj.published = True

        obj.save()


@admin.action(description="Toggle the tweeted status of posts")
def toggle_tweeted(modeladmin, request, queryset):
    for obj in queryset:
        obj.tweeted = not obj.tweeted
        obj.save()


@admin.action(description="Tweet this post")
def tweet_this_post(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.tweeted:
            tweet_new_post(obj, obj.tags.all())


@admin.action(description="Tweet this series")
def tweet_this_series(modeladmin, request, queryset):
    for obj in queryset:
        tweet_series(obj)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'likes',
                    'published', 'tweeted', 'timestamp', 'date_updated',)
    search_fields = ('title', 'author')
    ordering = ('-timestamp',)
    readonly_fields = ('slug', 'views',)
    list_filter = ('categories', 'tags', 'published')
    actions = [toggle_published, toggle_tweeted, tweet_this_post]


@admin.register(Series)
class SeriesAdmin(ModelAdmin):
    list_display = ('id', 'name', 'user', 'date_created', 'date_updated',)
    search_fields = ('name',)
    ordering = ('-id',)
    readonly_fields = ('slug',)
    actions = [tweet_series]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Recurring)
admin.site.register(Comment)
admin.site.register(SubComment)
admin.site.register(Like)
admin.site.register(Notification)


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('id', 'name', 'email', 'timestamp',)
    ordering = ('-timestamp',)


@admin.register(BulletinSubscriber)
class BulletinSubscriberAdmin(ModelAdmin):
    list_display = ('id', 'name', 'email', 'subs_type', 'timestamp',)
    ordering = ('-timestamp',)
    list_filter = ('subs_type',)
