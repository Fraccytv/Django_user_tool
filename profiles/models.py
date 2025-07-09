from django.db import models
from accounts.models import CustomUser


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_email', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    # birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"