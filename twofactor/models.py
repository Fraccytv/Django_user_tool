from django.db import models
from accounts.models import CustomUser as User
# Create your models here.

class UserTwoFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Enabled' if self.is_enabled else 'Disabled'}"

    class Meta:
        verbose_name = "TwoFactorAuth"
        verbose_name_plural = "TwoFactorAuths"