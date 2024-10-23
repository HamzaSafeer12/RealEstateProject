from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    reset_pin = models.CharField(max_length=6, blank=True, null=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Real Estate Agent'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Make username non-unique and email unique
    username = models.CharField(max_length=150, unique=False)  # Username is not unique
    email = models.EmailField(unique=True)  # Email is unique

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Ensure username is still required for user creation
