from django.contrib import admin
from .models import Member, MemberProfile, Post

# Register your models here.
admin.site.register(Member)
admin.site.register(MemberProfile)
admin.site.register(Post)