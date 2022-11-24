import re
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

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
        # retrieve workouts
        workouts = Workout.objects.filter(user=member.id).order_by('-workout_date')
        # retreive workout ids for workouts
        workout_ids = workouts.values_list('id', flat=True)
        # retreive exercises for workout ids
        exercises = Exercise.objects.filter(workout_id__in=list(workout_ids))
        if workouts is not None and exercises is not None:
            workouts = serializers.serialize("json", workouts)
            exercises = serializers.serialize("json", exercises)
            context = {
                'workouts': workouts,
                'exercises': exercises,
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
            if num_reps is not "" and num_reps.isnumeric():
                set.num_repititions = int(num_reps)
            else:
                messages.error(request, 'There was an error setting the number of reps')
                return redirect(request.META['HTTP_REFERER'])
            if weight is not "":
                set.weight = weight
            else:
                messages.error(request, 'There was an error setting the weight for this set')
                return redirect(request.META['HTTP_REFERER'])
            set.notes = notes
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
        one_rep_maxes = OneRepMax.objects.filter(user=request.user.id)
        if request.method == 'POST':
            bench_press = request.POST.get("BenchPress-weight")
            squat = request.POST.get("Squat-weight")
            deadlift = request.POST.get("Deadlift-weight")
            print('printing bench:')
            print(bench_press)
            if bench_press is not "" and squat is not "" and deadlift is not "":
                bench_max = one_rep_maxes.get(exercise="Bench Press")
                squat_max = one_rep_maxes.get(exercise="Squat")
                deadlift_max = one_rep_maxes.get(exercise="Deadlift")
                bench_max.weight = bench_press
                squat_max.weight = squat
                deadlift_max.weight = deadlift
                bench_max.save()
                squat_max.save()
                deadlift_max.save()
                messages.success(request, 'One Rep Maxes updated successfully')
            else:
                messages.error(request, 'There was an error saving the One Rep Max Data.')
            return redirect(request.META['HTTP_REFERER'])