from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.contrib.auth import logout
from django.template import loader
from django.db import transaction
from main.models import Memes
from .models import Follow


# Login Page
def userLogin(request):
    return render(request, 'login.html')


# Logout Page
@login_required(login_url='users:user-login')
def userLogout(request):
    logout(request)
    return redirect('users:user-login')


# Follow Feature
@login_required(login_url='login')
def follow(request, username):
    user = request.user
    following = get_object_or_404(User, username=username)
    if user != following:
        follow_status = Follow.objects.filter(
            following=following, follower=user).exists()
        if follow_status == True:
            Follow.objects.filter(following=following, follower=user).delete()
        else:
            Follow.objects.create(following=following, follower=user)
        return HttpResponseRedirect(reverse('users:profile', args=[username]))
    else:
        return HttpResponseRedirect(reverse('users:profile', args=[username]))


# @login_required(login_url='login')
# def follow(request):
#     user = request.user
#     if request.POST.get('action') == 'post':
#         username = int(request.POST.get('username'))
#         following = get_object_or_404(User, username=username)
#         follow_status = Follow.objects.filter(
#             following=following, follower=user).exists()
#         if follow_status == True:
#             Follow.objects.filter(following=following, follower=user).delete()
#             result = False
#         else:
#             Follow.objects.create(following=following, follower=user)
#             result = True

#         return JsonResponse({'result': result, })


# User Profile Page
def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    template = loader.get_template('profile.html')
    user_posts = Memes.objects.filter(
        user=user).order_by('-date')
    follow_status = Follow.objects.filter(
        following=user, follower=request.user).exists()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    context = {
        'page_user': user,
        'user_posts': user_posts,
        'follow_status': follow_status,
        'following_count': following_count,
        'followers_count': followers_count
    }
    return HttpResponse(template.render(context, request))


# User Followers Page
def userProfileFollowers(request, username):
    user = get_object_or_404(User, username=username)
    template = loader.get_template('followers.html')
    followers = Follow.objects.filter(following=user)
    context = {
        'followers': followers,
        'page_user': user
    }
    return HttpResponse(template.render(context, request))


# User Following Page
def userProfilefollowing(request, username):
    user = get_object_or_404(User, username=username)
    template = loader.get_template('following.html')
    following = Follow.objects.filter(follower=user)
    context = {
        'following': following,
        'page_user': user
    }
    return HttpResponse(template.render(context, request))
