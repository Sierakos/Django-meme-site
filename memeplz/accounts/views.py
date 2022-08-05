from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from memes.models import Post, LikePost
from .forms import RegisterForm, LoginForm, ProfileForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Witaj')
                return redirect(reverse('memeplz:home'))
    else:
        form = LoginForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context=context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login'))
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context=context)     

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('memeplz:home'))

@login_required
def my_profile_view(request):
    # profile = Profile.objects.get(user=request.user)
    profile = get_object_or_404(Profile, user=request.user)
    posts = Post.objects.filter(author=request.user.profile)
    context = {
        'profile': profile,
        'posts': posts
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes
    return render(request, 'accounts/profile.html', context=context)

def profile_view(request, username):
    # profile = Profile.objects.get(user__username=username)
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=profile)
    context = {
        'profile': profile,
        'posts': posts
    }
    if request.user.is_authenticated:
        likes = LikePost.objects.filter(user=request.user)
        liked_posts = likes.values_list('post', flat=True)
        context['likes'] = liked_posts
        context['like'] = likes
    return render(request, 'accounts/another_profile.html', context=context)

@login_required
def change_profile_view(request):
    values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    form = ProfileForm(instance=request.user.profile, initial=values)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('image'):
                profile.image = form.cleaned_data.get('image')

            
            profile.save()
            profile.user.save()
            return redirect(reverse('accounts:my_profile'))
        

    return render(request, 'accounts/change_profile.html', context=context)

@login_required
def delete_account(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
    return redirect(reverse('memeplz:home'))