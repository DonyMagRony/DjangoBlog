from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .CBV import ProfileView,ProfileEditView
from .FBV import register,follow,unfollow,login_view,logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),  # Author profile 
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),  # Author profile
    path('my_profile/<str:username>/', ProfileView.as_view(), name='self_profile'),  # Self-profile
    path('my_profile/<str:username>/edit/', ProfileEditView.as_view(), name='profile_edit'),  # Edit profile
    path('follow/<str:username>/', follow, name='follow'),  # Follow profile
    path('unfollow/<str:username>/', unfollow, name='unfollow'),  # Unfollow profile
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)