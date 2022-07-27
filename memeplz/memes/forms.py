from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        field = ['title', 'image']
        exclude = ['author', 'likes', 'is_on_main_page']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        field = ['content']
        exclude = ['author', 'likes', 'post']