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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        # Fetch the user based on the username provided in the URL
        profile_user = get_object_or_404(User, username=username)  # Get the user by username
        profile = get_object_or_404(Profile, user=profile_user)  # Get the profile associated with that user
        
        # Get the list of followers for the profile user
        followers = Follow.objects.filter(following=profile_user).select_related('follower')

        return render(request, 'profile.html', {
            'user': profile_user,
            'profile': profile,
            'followers': followers,  # Pass the followers list to the template
        })


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, username):
        # Check if the requested profile belongs to the logged-in user
        if request.user.username != username:
            raise PermissionDenied  # or you can redirect to a different page

        profile = get_object_or_404(Profile, user=request.user)  # Fetch the user's profile
        form = ProfileForm(instance=profile)  # Create a form instance for the profile
        return render(request, 'profile_edit.html', {'form': form})  # Render the edit form

    def post(self, request, username):
        # Check if the requested profile belongs to the logged-in user
        if request.user.username != username:
            raise PermissionDenied  # or you can redirect to a different page
        
        profile = get_object_or_404(Profile, user=request.user)  # Fetch the user's profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Handle form submission with instance
        
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the updated profile
            messages.success(request, "Profile updated successfully!")  # Success message
            return redirect('profile', username=request.user.username)  # Redirect to the profile page using the username
        
        # If the form is invalid, render the form again with errors
        return render(request, 'profile_edit.html', {'form': form})