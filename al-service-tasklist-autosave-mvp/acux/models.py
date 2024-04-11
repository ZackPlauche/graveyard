from django.db import models
from django.contrib import admin

from .choices import PlatformVersion

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Service(BaseModel):
    name = models.CharField(max_length=100, default='New Service')
    platform_version = models.CharField(max_length=100, choices=PlatformVersion.choices, default=PlatformVersion.CHOICE_1)

    def __str__(self):
        return self.name


class Task(BaseModel):
    name = models.CharField(max_length=100, default='New Task')
    completed = models.BooleanField(default=False)
    
    provisioner_1 = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_tasks')
    provisioner_2 = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='assigned_tasks')
    service = models.ForeignKey('acux.Service', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name

    @property
    def version(self):
        return self.service.platform_version
