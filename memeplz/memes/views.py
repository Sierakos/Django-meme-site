from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from django.utils import timezone

from .models import Post, Comment, LikePost, LikeComment
from accounts.models import Profile

from .forms import CreatePostForm, CreateCommentForm

from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def home_view(request):

    search_post = request.GET.get('search')

    if search_post:
        posts = Post.objects.filter(
            title__icontains=search_post,
            created__lte=timezone.now(),
            is_on_main_page=True,
            ).order_by('-created')
        paginator = Paginator(posts, 500)
    else:
        posts = Post.objects.filter(
            created__lte=timezone.now(),
            is_on_main_page=True,
            ).order_by('-created')
        paginator = Paginator(posts, 5)

    top_ten_posts = Post.objects.filter(
        is_on_main_page=True,
        created__gte=timezone.now()-timedelta(days=7)
    ).order_by('-likes')[:3]

    page_obj = paginator.get_page(1)

    context = {
        'posts': posts,
        'top_ten_posts': top_ten_posts,
        'page_obj': page_obj,
        'next_page': 2,
        'previous_page': None,
        'last_page': paginator.num_pages,
        'home_main': True 
    }

    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes
    return render(request, 'memes/home.html', context=context)

def home_view_page(request, page):
    posts = Post.objects.filter(
        created__lte=timezone.now(),
        is_on_main_page=True,
        ).order_by('-created')
    paginator = Paginator(posts, 5)

    page_obj = paginator.get_page(page)

    context = {
        'posts': posts,
        'page_obj': page_obj,
        'next_page': page+1,
        'previous_page': page-1,
        'last_page': paginator.num_pages,
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes

    # Return to home (delete str/1 from url) when on first page
    if page == 1:
        return redirect(reverse('memeplz:home'))
    return render(request, 'memes/home.html', context=context)

def search_view(request, name, page):
    posts = Post.objects.filter(
            # created__gte=start_date(),
            # created__lte=end_date(),
            title__contains=name,
            is_on_main_page=True,
            ).order_by('-likes')

    paginator = Paginator(posts, 5)

    page_obj = paginator.get_page(page)

    context = {
        'posts': posts,
        'page_obj': page_obj,
        'next_page': page+1,
        'previous_page': page-1,
        'last_page': paginator.num_pages,
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes

    return render(request, 'memes/search.html', context=context)

def filtering_main_page(request, page):
    if request.method == "GET":
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        posts = Post.objects.filter(
            # created__gte=start_date(),
            # created__lte=end_date(),
            created__range=(start_date, end_date),
            is_on_main_page=True,
            ).order_by('-likes')
        paginator = Paginator(posts, 1)

        page_obj = paginator.get_page(page)

        context = {
            'posts': posts,
            'page_obj': page_obj,
            'next_page': str(int(page) +1),
            'previous_page': str(int(page) -1),
            'last_page': paginator.num_pages,
            'start_date': start_date,
            'end_date': end_date
        }
        if request.user.is_authenticated:
            likes = LikePost.objects.filter(user=request.user)
            liked_posts = likes.values_list('post', flat=True)
            context['likes'] = liked_posts
            context['like'] = likes

        print(start_date)
        print(end_date)


        return render(request, 'memes/home_filter.html', context=context)

def waiting_view(request):
    posts = Post.objects.filter(
        created__lte=timezone.now(),
        is_on_main_page=False,
        ).order_by('-created')
    paginator = Paginator(posts, 5)

    page_obj = paginator.get_page(1)

    context = {
        'posts': posts,
        'page_obj': page_obj,
        'next_page': 2,
        'previous_page': None,
        'last_page': paginator.num_pages
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes
    return render(request, 'memes/waiting.html', context=context)

def waiting_view_page(request, page):
    posts = Post.objects.filter(
        created__lte=timezone.now(),
        is_on_main_page=False,
        ).order_by('-created')
    paginator = Paginator(posts, 5)

    page_obj = paginator.get_page(page)

    context = {
        'posts': posts,
        'page_obj': page_obj,
        'next_page': page+1,
        'previous_page': page-1,
        'last_page': paginator.num_pages
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes
    return render(request, 'memes/waiting.html', context=context)

def detail_view(request, title, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-pk')
    form = CreateCommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    if request.user.is_authenticated:
        likes_comments = LikeComment.objects.filter(user=request.user)
        liked_comments = likes_comments.values_list('comment', flat=True)
        context['liked_comments'] = liked_comments
        context['likes_comments'] = likes_comments

        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes

        profile = Profile.objects.get(user=request.user)

        print(likes_comments)
        print(likes)

        if request.method == 'POST':
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                form.instance.author = profile
                form.instance.post = post
                form.save()

    return render(request, 'memes/detail.html', context=context)

@login_required
def add_meme_to_main_page(request, pk):
    post = Post.objects.get(pk=pk)
    post.is_on_main_page = True
    post.save()
    return redirect(reverse('memeplz:waiting'))

@login_required
def create_post_view(request):
    form = CreatePostForm()
    profile = Profile.objects.get(user=request.user)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = profile
            form.save()
            return redirect(reverse('memeplz:home'))
        else:
            print('no valid')
    return render(request, 'memes/add_post.html', context=context)

@login_required
def like_unlike_post_view(request, pk):
    if request.method == 'POST':
        post = Post.objects.filter(pk=pk)
        already_liked = LikePost.objects.filter(user=request.user, post=post[0])
        if already_liked:
            LikePost.objects.filter(user=request.user, post=post[0]).delete()
            post_like = Post.objects.get(pk=pk)
            post_like.likes -= 1
            post_like.save()
            return redirect(reverse('memeplz:home'))
        else:
            like = LikePost.objects.create(user=request.user, post=post[0])
            like.save()
            post_like = Post.objects.get(pk=pk)
            post_like.likes += 1
            post_like.save()
            return redirect(reverse('memeplz:home'))

@login_required
def like_unlike_comment_view(request, pk):
    if request.method == 'POST':
        comment = Comment.objects.filter(pk=pk)
        already_liked = LikeComment.objects.filter(user=request.user, comment=comment[0])
        if already_liked:
            LikeComment.objects.filter(user=request.user, comment=comment[0]).delete()
            comment_like = Comment.objects.get(pk=pk)
            comment_like.likes -= 1
            comment_like.save()
            return redirect(reverse('memeplz:home'))
        else:
            like = LikeComment.objects.create(user=request.user, comment=comment[0])
            like.save()
            comment_like = Comment.objects.get(pk=pk)
            comment_like.likes += 1
            comment_like.save()
            return redirect(reverse('memeplz:home'))

@login_required
def delete_meme(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect(reverse('accounts:my_profile'))