from django.db import models
from django.conf import settings


class Reminder(models.Model):
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
