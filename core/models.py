from django.urls import reverse
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from authentication.models import Account


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=127)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    def natural_key(self):
        return (self.name)


class Tag(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name_plural = 'tags'
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('tag', args=[self.name])

    def natural_key(self):
        return (self.name)


class Post(models.Model):
    title = models.CharField(max_length=127)
    seo_overview = models.TextField()
    canonical_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    content = RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="blog/thumbnails")
    published = models.BooleanField(default=True)
    tweeted = models.BooleanField(default=False)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('single', args=[self.id, self.slug])


class Series(models.Model):
    name = models.CharField(max_length=127)
    desc = models.TextField(null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    thumbnail = models.ImageField(upload_to="blog/series")
    posts = models.ManyToManyField(
        Post, related_name='post_series', blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'series'
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Series, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('series', args=[self.id, self.slug])


class Like(models.Model):
    user = models.ManyToManyField(Account, related_name='liking_user')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    @classmethod
    def like(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(user)

    @classmethod
    def dislike(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(user)

    def __str__(self) -> str:
        return f'{self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
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


class Recurring(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f"{self.name}"


class BulletinSubscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subs_type = models.ForeignKey(Recurring, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.email}"


class Notification(models.Model):
    # 1 : Like, 2: Comment, 3: Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(
        Account, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(
        Account, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)
