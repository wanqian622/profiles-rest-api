from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom model."""
    # A help function to tell django to create a user without custom user
    # model
    def create_user(self, email, name, password=None):
        """ Creates a new user profile object."""
        # check the email address
        if not email:
            raise ValueError('Users must have an email address.')

        # Normalizing the email address
        # It converts all of characters to lowercase
        email = self.normalize_email(email)

        # Create a new user profile objects
        user = self.model(email=email, name=name)

        # Set user's password
        # convert the string that they provided as password to a hash
        # which is stored in the database
        user.set_password(password)

        # Save the model
        user.save(using=self._db)

        return user

    # A help function to tell django to create a super user
    def create_superuser(self, email, name, password):
        """ Creates and saves a new superuser with given details"""
        # Create a normal user first, then change it to the super user
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user





class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a "user UserProfile" inside our system"""
    # Four fields: email, name, is_active, is_staff
    # field for email
    email = models.EmailField(max_length=255, unique=True)
    # field for name
    name = models.CharField(max_length=255)
    # is_active is used to determine whether this paritular user is
    # currently active in the system
    is_active = models.BooleanField(default=True)
    # is_staff filed
    is_staff = models.BooleanField(default=False)

    # Set an object manager, an object manager is another class
    # that we can use to help manage the user profiles
    # It will give us some extra functionality like creating
    # an administrator user or a regular user
    objects = UserProfileManager()

    # couple more attributes that we need to set
    # USERNAME_FIELD the filed that is going to be used as the user name
    USERNAME_FIELD = 'email'
    # Required fields, a list of fields that are required for all user profile objects
    # in the system
    REQUIRED_FIELDS = ['name']

    # couple of helper functions for our models
    def get_full_name(self):
        """ Used to get a user's full name. """
        return self.name

    def get_short_name(name):
        """ Used to get a user's short name. """
        return self.name

    # STR: return our object as a string
    def __str__(self):
        """ Django uses this when it needs to convert the object to a string. """
        return self.email
