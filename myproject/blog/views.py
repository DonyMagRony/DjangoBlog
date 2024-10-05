from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse, JsonResponse 
from .models import Post,Comment
from .forms import CommentForm, NewPostForm
from .serializers import PostSerializer
from django.contrib.auth.mixins import LoginRequiredMixin


class PostsListCreateView(LoginRequiredMixin,View):
    template_name = 'post_list.html'
    
    def get(self, request):
        posts = Post.objects.all()
        form = NewPostForm()
        context = {
            'posts': posts,
            'form': form  # Include the form for creating new posts
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')  # After creating a post, redirect to the posts list
        context = {
            'posts': Post.objects.all(),
            'form': form  # Re-render form with errors if invalid
        }
        return render(request, self.template_name, context)


class PostDetailView(LoginRequiredMixin,View):
    template_name = 'post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()  # Fetch comments for the post
        comment_form = CommentForm()  # Empty form for adding comments
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
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
   
class PostUpdateView(LoginRequiredMixin, View):
    template_name = 'post_form.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = NewPostForm(instance=post)  # Pre-fill the form with post data
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = NewPostForm(request.POST, instance=post)  # Bind form to the post instance
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)

