from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

# 💡 Notes:
# - Passwords are encrypted using Fernet (not Django's default hashing)
# - This is a custom auth system — not based on Django's AbstractBaseUser
# - You must implement login/session tracking manually
