import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Announcement, Workout, User, Exercise, Set, OneRepMax

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
    else:
        return render(request, 'base/404.html', context={
            'msg': 'You must be logged in to view Your Workouts'
        })

def workout(request, pk):
    workout = Workout.objects.get(id=pk)
    if workout is not None:
        exercises = Exercise.objects.filter(workout=pk)
        for exercise in exercises:
            sets = Set.objects.filter(exercise=exercise.id)
            exercise.sets = sets
        context = {
            'workout': workout,
            'exercises': exercises,
            'range': range(1, 13)
        }
        return render(request, 'base/workout.html', context)
    else: 
        return render(request, 'base/404.html', context={
            'msg': 'It looks like you do not have any Workouts scheduled'
        })

""" Method to update set """
# TODO: needs improvements... this is messy logic
def update_set(request, pk):
    if request.method == 'POST':
        set = Set.objects.get(id=pk)
        if set is not None:
            num_reps = request.POST.get("num_repititions")
            weight = request.POST.get("weight")
            notes = request.POST.get("notes")
            if num_reps is not None and num_reps.isnumeric():
                set.num_repititions = int(num_reps)
            else:
                messages.error(request, 'There was an error setting the number of reps')
                return redirect(request.META['HTTP_REFERER'])
            if weight is not None:
                set.weight = weight
            else:
                messages.error(request, 'There was an error setting the weight for this set')
                return redirect(request.META['HTTP_REFERER'])
            if notes is not None and isinstance(notes, str):
                set.notes = notes
            else:
                messages.error(request, 'There was an error setting the set notes for this set')
                return redirect(request.META['HTTP_REFERER'])
            set.save()
            messages.success(request, 'Set updated successfully')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'There was an error saving the Set details. Please try again')

def one_rep_max(request):
    if request.user.is_authenticated:
        member = request.user
        one_rep_maxes = OneRepMax.objects.filter(user=member.id)
        if one_rep_maxes is not None:
            context = {
                'oneRepMaxes': one_rep_maxes
            }
        return render(request, 'base/one_rep_max.html', context)
    else:
        return render(request, 'base/404.html', context={
            'msg': 'You must be logged in to view your One Rep Maxes'
        })

def update_one_rep_maxes(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect(request.META['HTTP_REFERER'])