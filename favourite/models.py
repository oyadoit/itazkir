from django.db import models
from django.conf import settings


class Favourite(models.Model):
    content = models.ForeignKey('content.Content', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)