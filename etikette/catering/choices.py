from django.db import models

class Tier(models.TextChoices):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'