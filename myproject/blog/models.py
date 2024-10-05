from django.db import models
from django.contrib.auth.models import User

# Post model
class Post(models.Model):
    class Meta:
        db_table = "post"

    title = models.CharField(
        'Title',
        max_length=255,  # Set a max_length for CharField
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
        auto_now_add=True  # Automatically set the field to now when the object is first created
    )
    author = models.ForeignKey(
        User,  # Reference to Django's built-in User model
        on_delete=models.CASCADE,  # If the user is deleted, their posts are deleted as well
        related_name='posts'  # Related name to easily access the posts from the User model
    )

    def __str__(self):
        return self.title

# Comment model
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
        auto_now_add=True  # Automatically set the field to now when the comment is created
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # If the related post is deleted, the comments are deleted too
        related_name='comments'  # Related name to easily access comments from the Post model
    )
    author = models.ForeignKey(
        User,  # Reference to Django's built-in User model
        on_delete=models.CASCADE,  # If the user is deleted, their comments are deleted too
        related_name='comments'  # Related name to access user comments
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
