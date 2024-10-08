from rest_framework import serializers
from .models import Post, Comment  
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)  
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)  
    post_title = serializers.CharField(source='post.title', read_only=True) 

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author']
