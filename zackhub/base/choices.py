from django.db.models import TextChoices

class Alignment(TextChoices):
    LEFT = 'text-left'
    CENTER = 'text-center'
    RIGHT = 'text-right'