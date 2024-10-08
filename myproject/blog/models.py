from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    class Meta:
        db_table = "post"

    title = models.CharField(
        'Title',
        max_length=255,  
        unique=False,
        blank=False,
        null=False
    )
    content = models.TextField(
        'Content',
        unique=False,
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,  
        on_delete=models.CASCADE,  
        related_name='posts'  
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        db_table = "comment"

    content = models.TextField(
        'Content',
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True  
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  
        related_name='comments' 
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'  
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
