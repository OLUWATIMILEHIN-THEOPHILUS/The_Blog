from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    avatar = models.ImageField(
        upload_to='avatars', null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):
    heading = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='pics', null=True, default='post-avatar1.png')
    detail = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-posted']

    def __str__(self):
        return self.heading[0:50]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    sent = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited', '-sent']

    def __str__(self):
        return self.body[0:30]
