from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from . import models



class Signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = serializers.MemberSignupSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            raw_password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')

            hashed_password = make_password(raw_password)
            user_exists = models.Member.objects.filter(username=username)
            if user_exists:
                return Response({'error': 'user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(password=hashed_password)
            return Response({'message': 'signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = serializers.MemberLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = models.Member.objects.get(username=username)
            except models.Member.DoesNotExist:
                user = None

            if user is not None and check_password(password, user.password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'login successful',
                                 'access_token': token.key}, status=status.HTTP_200_OK)    
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = serializers.ProfileSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            member_profile, created = models.MemberProfile.objects.get_or_create(user=user)

            member_profile.phone_number = serializer.validated_data.get('phone_number')
            member_profile.location = serializer.validated_data.get('location')
            member_profile.bio = serializer.validated_data.get('bio')

            member_profile.save()
            return Response({'message': 'Profile data created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
