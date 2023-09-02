from rest_framework import serializers
from .models import Member, MemberProfile


class MemberSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['phone_number', 'location', 'bio']