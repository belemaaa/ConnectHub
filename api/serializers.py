from rest_framework import serializers
from .models import Member, MemberProfile, Post, Like, Comment


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
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'owner']

    def get_owner(self, obj):
        return {
            'user_id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.memberprofile.first_name,
            'last_name': obj.user.memberprofile.last_name,
            'phone_number': obj.user.memberprofile.phone_number,
            'location': obj.user.memberprofile.location,
            'bio': obj.user.memberprofile.bio
        }

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'