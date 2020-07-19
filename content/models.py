from django.db import models
from django.conf import settings

from core.models import ModelWithTimeStamp


class Content(ModelWithTimeStamp):
    reminder = models.ForeignKey('reminder.Reminder', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    data = models.TextField(null=True)
    content_image = models.CharField(max_length=200, null=True)
