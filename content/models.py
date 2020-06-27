from django.db import models
from django.conf import settings



class Content(models.Model):
    reminder = models.ForeignKey('reminder.Reminder', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    data = models.TextField()
    content_image = models.CharField(max_length=200, null=True)
