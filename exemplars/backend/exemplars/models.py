from django.db import models


class Exemplar(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    favorite = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
