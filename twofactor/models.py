from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserTwoFactor(models.Model):
    # Generic relation så app'en kan bruges uden Django auth.User eller en bestemt user-model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)  # understøtter str/int UUID etc.
    user = GenericForeignKey("content_type", "object_id")

    secret_key = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id"],
                name="uniq_user_twofactor_per_user",
            ),
        ]
        verbose_name = "Two-Factor Auth"
        verbose_name_plural = "Two-Factor Auth"

    def __str__(self) -> str:  # pragma: no cover
        status = "Enabled" if self.is_enabled else "Disabled"
        ident = (
            getattr(self.user, "username", None)
            or getattr(self.user, "email", None)
            or str(self.object_id)
        )
        return f"{ident} - {status}"


class BackupCode(models.Model):
    twofactor = models.ForeignKey(
        UserTwoFactor, on_delete=models.CASCADE, related_name="backup_codes"
    )
    code = models.CharField(max_length=64, db_index=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["twofactor", "code", "used"])]

    def __str__(self) -> str:  # pragma: no cover
        status = "Used" if self.used else "Unused"
        ident = (
            getattr(self.twofactor.user, "username", None)
            or getattr(self.twofactor.user, "email", None)
            or str(self.twofactor.object_id)
        )
        return f"Backup({ident}) - {status}"
