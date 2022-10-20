from enum import unique
from unicodedata import name
from uuid import UUID
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class User(AbstractBaseUser):
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    email_address = models.EmailField(
        verbose_name = 'email address',
        max_length = 255,
        unique = True
    )
    # Staff and Admin privileges
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email_address'  

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return name

    @property
    def is_staff(self):
        "Is the User a staff member?"
        return self.staff
    
    @property
    def is_admin(self):
        "Is the User an administrator?"
        return self.admin


class UserManager(BaseUserManager):
    def create_user(self, email_address, password=None):
        """ create and save a User with the given email and password """
        if not email_address:
            raise ValueError('User must have an email address')
        
        user = self.model(
            email_address = self.normalize_email(email_address)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff_user(self, email_address, password):
        """ create and save a staff User with email and p/w """
        user = self.create_user( 
            email_address, 
            password = password
        )
        user.staff = True
        user.save(using = self._db)
        return user

    def create_admin_user(self, email_address, password):
        """ creates admin User with email and p/w """
        user = self.create_user(
            email_address,
            password = password
        )
        user.staff = True
        user.admin = True
        user.save(using = self._db)
        return user

class Workout(models.Model):
    workout_name = models.CharField(null=False, max_length=255)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    workout_date = models.DateTimeField()
    # list of exercises

    def __str__(self):
        return '{}: {}'.format(str(self.workout_id), self.workout_name)

class Exercise(models.Model):
    exercise_name = models.CharField(null=False, max_length=255)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    exercise_date = models.DateTimeField()
    # foreign key relationship: one Workout can have many exercises
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(str(self.exercise_id), self.exercise_name)

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
        return '{}: {}'.format(str(self.set_id), self.set_number)


