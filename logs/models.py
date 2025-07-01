from django.db import models
from accounts.models import User
from django.utils import timezone


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10)
    event_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)