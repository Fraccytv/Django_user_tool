import os, hashlib, hmac
from binascii import hexlify, unhexlify
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

def generate_salt(n_bytes: int = 16) -> str:
    return hexlify(os.urandom(n_bytes)).decode("ascii")

def hash_password(raw_password: str, salt_hex: str, iterations: int = 260000) -> str:
    salt = unhexlify(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode("utf-8"), salt, iterations)
    return hexlify(dk).decode("ascii")

def verify_password(raw_password: str, salt_hex: str, stored_hash_hex: str, iterations: int = 260000) -> bool:
    salt = unhexlify(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(hexlify(dk).decode("ascii"), stored_hash_hex)


from .models import LoginAttempt, CustomUser

FAIL_LIMIT  = getattr(settings, "LOGIN_FAIL_LIMIT", 5)
FAIL_WINDOW = timedelta(minutes=getattr(settings, "LOGIN_FAIL_WINDOW_MIN", 15))
LOCKOUT_LEN = timedelta(minutes=getattr(settings, "LOGIN_LOCKOUT_MIN", 15))

def get_or_create_attempt(user: CustomUser) -> LoginAttempt:
    obj, _ = LoginAttempt.objects.get_or_create(
        user=user,
        defaults={
            "failed_attempts": 0,
            "last_attempt": timezone.now(),
        },
    )
    return obj

def is_locked(user: CustomUser) -> bool:
    la = get_or_create_attempt(user)
    return la.locked_until is not None and la.locked_until > timezone.now()

@transaction.atomic
def register_failed_attempt(user: CustomUser, ip: str | None = None) -> None:
    now = timezone.now()
    la, _ = LoginAttempt.objects.select_for_update().get_or_create(
        user=user,
        defaults={
            "failed_attempts": 0,
            "last_attempt": now - (FAIL_WINDOW + timedelta(seconds=1)),
        },
    )

    # reset hvis uden for vindue; ellers +1
    if la.last_attempt is None or (now - la.last_attempt) > FAIL_WINDOW:
        la.failed_attempts = 1
    else:
        la.failed_attempts += 1

    la.last_attempt = now
    if ip:
        la.ip_address = ip

    if la.failed_attempts >= FAIL_LIMIT:
        la.locked_until = now + LOCKOUT_LEN

    la.save(update_fields=["failed_attempts", "last_attempt", "ip_address", "locked_until"])

@transaction.atomic
def reset_attempts(user: CustomUser) -> None:
    la, _ = LoginAttempt.objects.select_for_update().get_or_create(
        user=user,
        defaults={"failed_attempts": 0, "last_attempt": timezone.now()},
    )
    la.failed_attempts = 0
    la.locked_until = None
    la.save(update_fields=["failed_attempts", "locked_until"])