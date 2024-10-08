from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .models import Profile,Follow
from .forms import UserRegisterForm,ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm  # Optional: for using built-in form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from functools import lru_cache
class BaseProfileView(View):
    def get_profile_user(self, username):
        return get_object_or_404(User, username=username)

    def get_profile(self, user):
        return get_object_or_404(Profile, user=user)
    

class ProfileView(LoginRequiredMixin, View):
    @lru_cache(maxsize=15)
    def get(self, request, username=None):
        if username:
            profile_user = self.get_profile_user(username)
            profile = self.get_profile(profile_user)
            
            followers = Follow.objects.filter(following=profile_user).select_related('follower')
            is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

            return render(request, 'profile.html', {
                'user': profile_user,
                'profile': profile,
                'followers': followers,
                'following':following,
                'is_following': is_following,
            })
        else:
            all_profiles = Profile.objects.exclude(user=request.user)  
            return render(request, 'profiles.html', {
                'profiles': all_profiles,
            })

    def get_profile_user(self, username):
        from django.contrib.auth.models import User
        return User.objects.get(username=username)

    def get_profile(self, user):
        return Profile.objects.get(user=user)


class ProfileEditView(LoginRequiredMixin, BaseProfileView):
    def get(self, request, username):
        if request.user.username != username:
            raise PermissionDenied
        
        profile_user = self.get_profile_user(username)
        profile = self.get_profile(profile_user)
        form = ProfileForm(instance=profile)
        
        return render(request, 'profile_edit.html', {'form': form})

    def post(self, request, username):
        if request.user.username != username:
            raise PermissionDenied
        
        profile_user = self.get_profile_user(username)
        profile = self.get_profile(profile_user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile', username=request.user.username)
        
        return render(request, 'profile_edit.html', {'form': form})
