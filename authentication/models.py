from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class SocialLinks(models.Model):
    youtube_url = models.URLField(verbose_name='youtube link', blank=True)
    facebook_url = models.URLField(verbose_name='facebook link', blank=True)
    instagram_url = models.URLField(verbose_name='instagram link', blank=True)
    dribble_url = models.URLField(verbose_name='dribble link', blank=True)
    github_url = models.URLField(verbose_name='github link', blank=True)
    gitlab_url = models.URLField(verbose_name='gitlab link', blank=True)
    medium_url = models.URLField(verbose_name='medium link', blank=True)
    twitter_url = models.URLField(verbose_name='twitter link', blank=True)
    linkedin_url = models.URLField(verbose_name='linkedin link', blank=True)
    portfolio_url = models.URLField(verbose_name='portfolio link', blank=True)

    class Meta:
        verbose_name_plural = 'Social Links'


class Work(models.Model):
    employer_title = models.CharField(max_length=127, blank=True)
    employer_name = models.CharField(max_length=127, blank=True)
    education = models.CharField(max_length=127, blank=True)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              max_length=127, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="authentication/profile_images", default="authentication/profile_images/favicon-512.png")
    location = models.CharField(max_length=63)
    social_links = models.ForeignKey(
        SocialLinks, on_delete=models.PROTECT, blank=True, null=True)
    work = models.ForeignKey(
        Work, on_delete=models.PROTECT, blank=True, null=True)
    pwd_changed = models.BooleanField(default=False)
    pwd_mail_sent = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    # For checking permissions. to keep it simple all admin have ALL permissons

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# For OTP
class OTPModel(models.Model):
    user = models.EmailField(max_length=127)
    timestamp = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField()

    class Meta:
        verbose_name = 'OTP'


# For Follow Model
class FollowersModel(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    following = models.ManyToManyField(Account, related_name='following')
    follower = models.ManyToManyField(Account, related_name='follower')

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.following.add(another_account)

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.following.remove(another_account)

    def __str__(self) -> str:
        return f'{self.user}'