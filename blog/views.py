from django.shortcuts import render, get_object_or_404
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages, sessions
from .models import FirstVsit, Profile, Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.db.models import F, Sum
import datetime


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:

                    login(request, user)
                    # to check if a user have login before
                    if request.session is None:
                        user_point = Profile.objects.get(user=request.user)
                        user_point.points = F('points') + 100
                        user_point.save()

                        request.session.set_expiry(86400)
                        return HttpResponse('You have earned 100points for daily login')
                    else:
                        return HttpResponse('you have earned your point for today')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid account')
    else:
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def index_details(request, slug):
    post_details = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/details.html', {'details': post_details})


# to check if a user have read a post
@login_required
def link_click(request):
    if not FirstVsit.objects.filter(user=request.user.id, url=request.path).exists():
        user_point = Profile.objects.get(user=request.user)
        user_point.points = F('points') + 50
        user_point.save()

        FirstVsit(user=request.user, url=request.path).save()
        return HttpResponse('you have earned 50points for reading this post')


# to return total points gain
@login_required
def profile_view(request):
    earnings = Profile.objects.aggregate(Sum('points'))
    return render(request, 'account/profile.html', {'total_earnings': earnings})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated sucessfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
