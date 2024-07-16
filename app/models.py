from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=200, unique=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{get_random_string(4)}'
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )


class Scrap(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="scraps"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scraps"
    )
