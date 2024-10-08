from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse, JsonResponse 
from .models import Post,Comment
from .forms import CommentForm, NewPostForm
from .serializers import PostSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from functools import lru_cache


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
    paginate_by = 1
    
    @lru_cache(maxsize=15)
    def get_posts(self, request):
        title_query = request.GET.get('title', '')
        author_query = request.GET.get('author', '')
        user_posts = Post.objects.filter(author=request.user).order_by('title')
        other_posts = Post.objects.exclude(author=request.user).order_by('title')

        if title_query:
            user_posts = user_posts.filter(title__icontains=title_query)
            other_posts = other_posts.filter(title__icontains=title_query)

        if author_query:
            user_posts = user_posts.filter(author__username__icontains=author_query)
            other_posts = other_posts.filter(author__username__icontains=author_query)

        post_list = list(user_posts) + list(other_posts)
        paginator = Paginator(post_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj

    @lru_cache(maxsize=10)
    def get(self, request):
        posts = self.get_posts(request)
        form = NewPostForm()
        context = {
            'posts': posts,
            'form': form ,
            'page_obj':posts
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user  
            post.save()  
            return redirect('posts')  
        context = {
            'posts': self.get_posts(request),
            'form': form  ,
            'title_query': request.GET.get('title', ''),
            'author_query': request.GET.get('author', '')
        }
        return render(request, self.template_name, context)


class PostDetailView(BasePostView):
    template_name = 'post_detail.html'
    
    def get(self, request, pk):
        post = self.get_post(pk)
        comments = post.comments.all()  
        comment_form = CommentForm()  
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
            comment.post = post  
            comment.author = request.user  
            comment.save()
            return redirect('post_detail', pk=post.pk)  
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
        form = NewPostForm(instance=post) 
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = self.get_post(pk)
        form = NewPostForm(request.POST, instance=post)  
        if form.is_valid():
            updated_post = form.save(commit=False)  
            updated_post.author = post.author  
            updated_post.save()  
            return redirect('post_detail', pk=post.pk)
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)
