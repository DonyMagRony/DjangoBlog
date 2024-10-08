from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'  
    )
    bio = models.TextField(
        'Bio',
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        'Profile Picture',
        upload_to='profile_pictures/',
        blank=True,
        null=False,
        default='profile_pictures/default.jpg' 
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following', 
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers', 
    )
    created_at = models.DateTimeField(auto_now_add=True)  
    class Meta:
        unique_together = ('follower', 'following')  

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"