from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    username = None
    email = models.EmailField('email address', unique=True)
    avatar = models.ImageField(upload_to='profile_pictures/', default='https://via.placeholder.com/400')

    objects = UserManager()

    def __str__(self):
        return self.email


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message