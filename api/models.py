from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

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