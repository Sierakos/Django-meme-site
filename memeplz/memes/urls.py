from django.urls import path

from . import views

app_name = 'memeplz'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('waiting-room', views.waiting_view, name='waiting'),
    path('detail/<str:title>/<int:pk>', views.detail_view, name='detail'),
    path('add-meme', views.create_post_view, name='create_post'),
    path('like_unlike/<int:pk>', views.like_unlike_post_view, name='like_unlike'),
    path('like_unlike_comment/<int:pk>', views.like_unlike_comment_view, name='like_unlike_comment'),
    path('add-meme-to-main-page/<int:pk>', views.add_meme_to_main_page, name='move_meme'),
]