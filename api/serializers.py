from rest_framework import serializers
from .models import Member, MemberProfile, Post


class MemberSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['username', 'password', 'email']


class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['first_name', 'last_name', 'phone_number', 'location', 'bio']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at']