from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    avatar = models.ImageField(upload_to='profile_pictures/', default='https://via.placeholder.com/400')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email