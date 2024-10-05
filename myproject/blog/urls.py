
from django.contrib import admin
from django.urls import path
from .views import PostsListCreateView,PostDetailView,PostUpdateView

urlpatterns = [
    path('posts/', PostsListCreateView.as_view(), name='posts'),  # Post listing and creation
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Post detail with comments
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_form'),  # Post update form
]

