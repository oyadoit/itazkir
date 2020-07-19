from django.db import models
from django.conf import settings

from core.models import ModelWithTimeStamp


class Reminder(ModelWithTimeStamp):
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
