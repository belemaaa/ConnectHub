from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):
    phone_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class MemberProfile(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)