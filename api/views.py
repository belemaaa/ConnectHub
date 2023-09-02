from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from . import serializers
from . import models



class Signup(APIView):
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
                return Response({'message': 'login successful'}, status=status.HTTP_200_OK)    
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
