from django.contrib import admin
from .models import Post, Comment, LikePost, LikeComment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(LikeComment)
