from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from authentication.models import Account


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"{self.name}"


class Post(models.Model):
    title = models.CharField(max_length=127)
    seo_overview = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="blog/thumbnails")
    published = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


# Contact Form
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=127)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
