from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
STATUS = ((0, 'Draft'),
          (1, 'Publish'))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='')
    viewers = models.ManyToManyField(User, blank=True)
    commented = models.ManyToManyField(User, blank=True, related_name="commented")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.title)
            super(Post, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=200, help_text='enter your country name')
    points = models.IntegerField(default=0)
    last_login = models.DateField(blank=True, null=True)
    # photo = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.user.username


class FirstVsit(models.Model):
    url = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.CharField(max_length=5000, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text
