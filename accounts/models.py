from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    salt = models.CharField(max_length=255, blank=True, null=True)
    
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"