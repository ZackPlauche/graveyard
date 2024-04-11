from django.db.models import TextChoices


class PricingModel(TextChoices):
    HOURLY = 'Hourly'
    MONTHLY = 'Monthly'
    PROJECT = 'Project'


class CTA(TextChoices):
    LEARN_MORE = 'Learn More'
    SCHEDULE_APPOINTMENT = 'Schedule Appointment'