import csv
import datetime

from django.shortcuts import render, redirect
from django.conf import settings
from service.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from service.forms import PostForm, CommentForm, UserRegisterForm, MessageForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def about(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            try:
                send_mail(subject, body, settings.EMAIL_HOST_USER, [email_reciever], fail_silently=False)
                form.save()
            except Exception as err:
                print(str(err))
            return redirect('about')
    return render(request, "about.html", {'form':form})


class RegisterForm(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_message = '%(username)s was created succesfully'
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-pk']


class DetailPostView(DetailView):
    model = Post
    template_name = 'detail_post.html'


# class CreatePostView(PermissionRequiredMixin, CreateView):
#     permission_required = 'service.add_post'
#     model = Post
#     template_name = 'create_post.html'
#     form_class = PostForm

@login_required
@permission_required('service.add_post')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            if title != "POST":
                messages.error(request, 'Something went wrong')
                return redirect('index')
            # id = form.cleaned_data.get('pk')
            messages.success(request, f"Post {title} was created succesfully")
            return redirect('index')
    return render(request, 'create_post.html', {'form':form})


class UpdatePostView(PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_post'
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm


class DeletePostView(PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_post'
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


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        file = FileSystemStorage()
        name = file.save(uploaded_file.name, uploaded_file)
        context['url'] = file.url(name)
    return render(request, 'upload.html', context)

def download(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Created_at'])
    for row in Post.objects.all().values_list('title', 'description', 'created_at'):
        writer.writerow(row)
    filename = str(datetime.datetime.now()) + 'posts.csv'
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response