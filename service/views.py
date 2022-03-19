from django.shortcuts import render, redirect
from django.views import generic

from service.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from service.forms import PostForm, CommentForm, UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

class RegisterForm(CreateView):
    from_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-pk']


class DetailPostView(DetailView):
    model = Post
    template_name = 'detail_post.html'


class CreatePostView(CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)