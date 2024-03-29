from django.db import models
from django.conf import settings

from core.models import ModelWithTimeStamp


class Subscription(ModelWithTimeStamp):
    reminder = models.ForeignKey('reminder.Reminder', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['reminder', 'user']]
