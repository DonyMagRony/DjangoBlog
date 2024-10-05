from rest_framework import serializers
from .models import Post, Comment  # Assuming Post and Comment are in the same app

# Serializer for Post model
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)  # To include the author's username

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']

# Serializer for Comment model
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)  # To include the commenter's username
    post_title = serializers.CharField(source='post.title', read_only=True)  # To include the post title

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author']
