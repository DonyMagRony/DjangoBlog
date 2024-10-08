from django import forms
from .models import Post,Comment

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post  
        fields = ['title', 'content']  
        widgets = {
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 4})  
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols':30,'rows':4})
        }