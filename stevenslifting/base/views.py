import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Announcement, Workout, User, Exercise, Set

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

def workouts(request):
    if request.user.is_authenticated:
        member = request.user
        workouts = Workout.objects.filter(user=member.id)
        if workouts is not None:
            for workout in workouts:
                exercises = Exercise.objects.filter(workout=workout.id)
                workout.exercises = exercises
            
            context = {
                'workouts': workouts,
                'user': member
            }
        return render(request, 'base/workouts.html', context)

def workout(request, pk):
    workout = Workout.objects.get(id=pk)
    if workout is not None:
        exercises = Exercise.objects.filter(workout=pk)
        for exercise in exercises:
            sets = Set.objects.filter(exercise=exercise.id)
            exercise.sets = sets
        context = {
            'workout': workout,
            'exercises': exercises
        }
    return render(request, 'base/workout.html', context)

        