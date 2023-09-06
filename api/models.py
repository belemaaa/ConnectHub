from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Member(AbstractUser):
    def __str__(self):
        return self.username


class MemberProfile(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"
    

class Like(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)