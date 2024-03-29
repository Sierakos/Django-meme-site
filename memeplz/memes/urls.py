from django.urls import path, re_path

from . import views

app_name = 'memeplz'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('str/<int:page>', views.home_view_page, name='home_page'),
    path('waiting-room', views.waiting_view, name='waiting'),
    path('waiting-room/str/<int:page>', views.waiting_view_page, name='waiting_page'),
    path('detail/<str:title>/<int:pk>', views.detail_view, name='detail'),
    path('add-meme', views.create_post_view, name='create_post'),
    path('like_unlike/<int:pk>', views.like_unlike_post_view, name='like_unlike'),
    path('like_unlike_comment/<int:pk>', views.like_unlike_comment_view, name='like_unlike_comment'),
    path('add-meme-to-main-page/<int:pk>', views.add_meme_to_main_page, name='move_meme'),
    path('delete/meme/<int:pk>', views.delete_meme, name='delete_meme'),
    path('search/<str:name>/<int:page>', views.search_view, name='search_view'),
    # date-picker
    re_path(r'^filtering-main-site/(?P<page>\d+)/$', views.filtering_main_page, name='filtering_main_site'),
]