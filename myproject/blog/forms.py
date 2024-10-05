from django import forms
from .models import Post,Comment

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post  # Link this form to the Post model
        fields = ['title', 'content']  # Specify the fields you want in the form
        widgets = {
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 4})  # Smaller size
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols':30,'rows':4})
        }