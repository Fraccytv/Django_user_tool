# logs/models.py
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Log(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"
    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILURE, "Failure"),
    ]

    EVENT_LOGIN = "login"
    EVENT_LOGOUT = "logout"
    EVENT_REGISTER = "register"
    EVENT_CHOICES = [
        (EVENT_LOGIN, "Login"),
        (EVENT_LOGOUT, "Logout"),
        (EVENT_REGISTER, "Register"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="logs")
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["event_type", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.event_type} {self.status} @{self.timestamp:%Y-%m-%d %H:%M:%S}"