from enum import unique
from unicodedata import name
from django.db import models
from django.contrib.auth.models import (
    User, BaseUserManager, AbstractBaseUser
)

# Create your models here.

class Workout(models.Model):
    workout_name = models.CharField(null=False, max_length=255)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    workout_date = models.DateTimeField()
    # list of users
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.workout_name

class Exercise(models.Model):
    exercise_name = models.CharField(null=False, max_length=255)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    exercise_date = models.DateTimeField()
    # foreign key relationship: one Workout can have many exercises
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def __str__(self):
        return self.exercise_name

class Set(models.Model):
    set_number = models.IntegerField(default=1, null=False)
    num_repititions = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    notes = models.TextField(null=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    # foreign key relationship: one Exercise can have multiple sets
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.set_number)

class Announcement(models.Model):
    title = models.CharField(null=False, max_length=255)
    body = models.TextField(null=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class OneRepMax(models.Model):
    exercise = models.TextField(null=False)
    weight = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.exercise