from django import forms
from .models import Post,Comment

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post  # Link this form to the Post model
        fields = ['title', 'content', 'author']  # Specify the fields you want in the form
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']