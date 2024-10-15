"""
Database models for the core app.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,                            # Contains the methods for authentication, but does not provide the fields for the user model
    BaseUserManager,                             # Manager for custom user model. The Manager is the interface through which database query operations are provided to Django models
    PermissionsMixin                             # Contains functionality for handling permissions, and related fields
)


class UserManager(BaseUserManager):              # Custom user manager class
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)    # Creates a new user model
        user.set_password(password)                                             # Sets the password for the user model
        user.save(using=self._db)                                               # Saves the user model using the database
        return user

    def create_superuser(self, email, password):
        """ Creates and saves a new superuser """
        user = self.create_user(email, password)                                # Creates a new user model
        user.is_staff = True                                                    # Sets the user as a staff user
        user.is_superuser = True                                                # Sets the user as a superuser
        user.save(using=self._db)                                               # Saves the user model. Passing self._db allows using multiple databases
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)         # Email field for the user model
    name = models.CharField(max_length=255)                        # Name field for the user model
    is_active = models.BooleanField(default=True)                  # Field to determine if the user is active
    is_staff = models.BooleanField(default=False)                  # Field to determine if the user is a staff user

    objects = UserManager()                                       # Assign the custom user manager to the objects attribute

    USERNAME_FIELD = 'email'                                       # Field to use as the unique identifier for the user model