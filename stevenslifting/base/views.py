import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Announcement, Workout, User

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('homepage')

def home(request):
    announcements = Announcement.objects.all()
    context = {'announcements': announcements}
    return render(request, 'base/home.html', context)

def workout(request):
    if request.user.is_authenticated:
        member = request.user
        workouts = Workout.objects.filter(user=member.id)
        context = {
            'workouts': workouts,
            'user': member
        }
        return render(request, 'base/workouts.html', context)
    # else we want to show 404 page, TBD