from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .models import Profile,Follow
from .forms import UserRegisterForm,ProfileForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm  # Optional: for using built-in form
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request, *args, **kwargs):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)

        if user_form.is_valid() :
            user = user_form.save()  # Save the user to the database
            login(request, user)  # Log in the newly registered user
            Profile.objects.create(user=user)  
            return redirect('profile')  # Redirect to the profile page or another page

    else:
        user_form = UserRegisterForm()
    return render(request, 'register.html', {
        'user_form': user_form,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Create a form instance with the submitted data
        if form.is_valid():
            username = form.cleaned_data['username']  # Get the username
            password = form.cleaned_data['password']  # Get the password
            user = authenticate(username=username, password=password)  # Authenticate the user
            
            if user is not None:
                login(request, user)  # Log the user in
                return redirect(f'/users/my_profile/{user.username}/')  # Redirect to their profile
            else:
                messages.error(request, "Invalid username or password.")  # Handle authentication failure
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests

    return render(request, 'login.html', {'form': form}) 

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    # Prevent a user from following themselves
    if request.user == user_to_follow:
        return redirect('profile', username=username)

    # Create a follow relationship
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    return redirect('profile', username=username)  # Redirect back to the profile

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    # Prevent a user from unfollowing themselves
    if request.user == user_to_unfollow:
        return redirect('profile', username=username)

    # Remove the follow relationship
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    return redirect('profile', username=username)  # Redirect back to the profile

