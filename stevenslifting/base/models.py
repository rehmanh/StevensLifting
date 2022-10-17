from enum import unique
from unicodedata import name
from uuid import UUID
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class User(AbstractBaseUser):
    user_id = UUID
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