from django.db import models
from django.contrib.auth.models import User

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'  # Access profile via user.profile
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
        null=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',  # The users this user is following
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',  # The users following this user
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the follow happened

    class Meta:
        unique_together = ('follower', 'following')  # Ensures no duplicate follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"