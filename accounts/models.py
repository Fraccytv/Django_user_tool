from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"
