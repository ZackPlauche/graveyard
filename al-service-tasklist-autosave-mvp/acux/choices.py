from django.db import models


class PlatformVersion(models.TextChoices):
    CHOICE_1 = '1.0'
    CHOICE_2 = '2.0'
    CHOICE_3 = '3.0'