"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import PostsListCreateView,PostDetailView,PostUpdateView

urlpatterns = [
    path('posts/', PostsListCreateView.as_view(), name='posts'),  # Post listing and creation
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Post detail with comments
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_form'),  # Post update form
]

