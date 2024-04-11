from django.db import models


class ProjectRole(models.TextChoices):
    OWNER = 'Owner'
    COLLABORATOR = 'Collaborator'
    PARTNER = 'Partner'
    LEAD_DEVELOPER = 'Lead Developer'


class ProjectStatus(models.TextChoices):
    PROTOTYPE = 'Prototype'
    LIVE = 'Live'
    COMPLETED = 'Completed'
    IN_PROGRESS = 'In Progress'
    PAUSED = 'Paused'
    CONCEPT = 'Concept'


class OfferType(models.TextChoices):
    SERVICE = 'service'
    PRODUCT = 'product'
    PACKAGE = 'package'


class PricingModel(models.TextChoices):
    HOURLY = 'hourly'
    ONEOFF = 'oneoff'
    SUBSCRIPTION = 'subscription'
    CUSTOM = 'custom'

class RequestStatus(models.TextChoices):
    NEW = 'new'
    IN_PROGRESS = 'in progress'
    FULFILLED = 'fulfilled'