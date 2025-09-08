from django.utils import timezone
from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    salt = models.CharField(max_length=255, blank=False, null=False)
    encrypted_password = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"


class LoginAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # ← vigtig ændring
    failed_attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(default=timezone.now)         # ← god default
    locked_until = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} at {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["locked_until"]),
        ]