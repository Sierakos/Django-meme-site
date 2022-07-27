from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to="meme_images")
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    is_on_main_page = models.BooleanField(default=False)

    def __str__(self):
        return f'Author: {self.author}, Title: {self.title}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=False, null=False)
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Author: {self.author}, Content: {self.content}'

class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}, likes: {self.post.title}'

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}, likes: {self.comment.content}'