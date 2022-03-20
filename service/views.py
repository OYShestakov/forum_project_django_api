from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic
from service.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from service.forms import PostForm, CommentForm, UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'index.html')

@login_required()
def about(request):
    return render(request, 'about.html')

class RegisterForm(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-pk']


class DetailPostView(DetailView):
    model = Post
    template_name = 'detail_post.html'


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)