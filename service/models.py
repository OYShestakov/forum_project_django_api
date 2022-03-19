from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(verbose_name='Картинка', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('index')


class Comment(models.Model):
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.description}'

    def get_absolute_url(self):
        return reverse('index')