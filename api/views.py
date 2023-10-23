from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsPostOwner
from django.db.models import Q
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
    
class Personal_profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            member_profile, created = models.MemberProfile.objects.get_or_create(user=user)

            member_profile.first_name = serializer.validated_data.get('first_name')
            member_profile.last_name = serializer.validated_data.get('last_name')
            member_profile.phone_number = serializer.validated_data.get('phone_number')
            member_profile.location = serializer.validated_data.get('location')
            member_profile.bio = serializer.validated_data.get('bio')
            member_profile.save()
            return Response({'message': 'Profile data created' if created else 'Profile data updated.'}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        try:
            member_profile = models.MemberProfile.objects.get(user=user)
        except models.MemberProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_posts = models.Post.objects.filter(user=user)
        serializer = serializers.PostSerializer(user_posts, many=True) 
        profile_data = {
            'id': member_profile.user.id,
            'username': member_profile.user.username,
            'email': member_profile.user.email,
            'first_name': member_profile.first_name,
            'last_name': member_profile.last_name,
            'phone_number': member_profile.phone_number,
            'location': member_profile.location,
            'bio': member_profile.bio,
            'posts': serializer.data
        }
        return Response({'profile_data': profile_data}, status=status.HTTP_200_OK)
    
class Post(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostOwner]
    def post(self, request):
        serializer = serializers.PostSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data.get('content')
            serializer.save(user=self.request.user)
            return Response({'message': 'Post created successfully',
                             'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = models.Post.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        except models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
             
    def get(self, request):
        qs = models.Post.objects.all()
        data = serializers.PostSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
class UserProfileSearch(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        search_query = self.request.query_params.get('search_query', None)
        queryset = models.MemberProfile.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        user_posts = models.Post.objects.filter(user__memberprofile__in=queryset)
        serializer = serializers.ProfileSerializer(queryset, many=True)
        post_serializer = serializers.PostSerializer(user_posts, many=True)
        data = {
            'profile_data': serializer.data,
            'posts': post_serializer.data
        }   
        return Response(data, status=status.HTTP_200_OK)
     
class Comment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, post_id):
        try:
            post = models.Post.objects.get(pk=post_id)
        except models.Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment_text = serializer.validated_data.get('comment')
            comment = models.Comment.objects.create(user=self.request.user, post=post, text=comment_text)
            return Response({'message': 'Comment created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)