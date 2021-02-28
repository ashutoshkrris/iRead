from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Category, Tag, Post, Comment, SubComment, Contact


# Register your models here.
@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'views',
                    'published', 'timestamp',)
    search_fields = ('title', 'author')
    ordering = ('-timestamp',)
    readonly_fields = ('slug','views',)
    list_filter = ('categories', 'tags', 'published')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(SubComment)


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('id', 'name', 'email', 'timestamp',)
    ordering = ('-timestamp',)
