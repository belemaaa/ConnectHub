from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('profile/', views.Personal_profile.as_view()),
    path('posts/add/', views.Post.as_view()),
    path('posts/<int:pk>/delete', views.Post.as_view()),
    path('posts/', views.Post.as_view()),
    path('profile/search/', views.UserProfileSearch.as_view()),
]