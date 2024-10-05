from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse, JsonResponse 
from .models import Post,Comment
from .forms import CommentForm, NewPostForm
from .serializers import PostSerializer
from django.contrib.auth.mixins import LoginRequiredMixin



class BasePostView(LoginRequiredMixin, View):
    model = Post  # Base model for post views
    template_name = None  # To be defined in subclasses

    def get_posts(self):
        """Fetch all posts."""
        return self.model.objects.all()

    def get_post(self, pk):
        """Fetch a single post by primary key."""
        return get_object_or_404(self.model, pk=pk)
class PostsListCreateView(BasePostView):
    template_name = 'post_list.html'
    
    def get(self, request):
        posts = self.get_posts()
        form = NewPostForm()
        context = {
            'posts': posts,
            'form': form  # Include the form for creating new posts
        }
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to the database yet
            post.author = request.user  # Assign the current user as the author
            post.save()  # Now save it
            return redirect('posts')  # After creating a post, redirect to the posts list
        context = {
            'posts': self.get_posts(),
            'form': form  # Re-render form with errors if invalid
        }
        return render(request, self.template_name, context)


class PostDetailView(BasePostView):
    template_name = 'post_detail.html'

    def get(self, request, pk):
        post = self.get_post(pk)
        comments = post.comments.all()  # Fetch comments for the post
        comment_form = CommentForm()  # Empty form for adding comments
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = self.get_post(pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Associate the comment with the post
            comment.author = request.user  # Set the current user as the author
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirect back to the post detail
        # If the comment form is invalid, re-render with errors
        comments = post.comments.all()
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)
   
class PostUpdateView(BasePostView):
    template_name = 'post_form.html'

    def get(self, request, pk):
        post = self.get_post(pk)
        form = NewPostForm(instance=post)  # Pre-fill the form with post data
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = self.get_post(pk)
        form = NewPostForm(request.POST, instance=post)  # Bind form to the post instance
        if form.is_valid():
            updated_post = form.save(commit=False)  # Don't save to the database yet
            updated_post.author = post.author  # Keep the original author
            updated_post.save()  # Now save it
            return redirect('post_detail', pk=post.pk)
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)
