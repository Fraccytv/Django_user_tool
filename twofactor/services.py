from __future__ import annotations

import secrets
from io import BytesIO
from typing import List, Optional

import pyotp
import qrcode
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from .models import BackupCode, UserTwoFactor
from .utils import encode_data_uri


def _ct_pk_for(user):
    """Find ContentType + objekt-id for vilkårlig brugermodel.
    Hvorfor: Gør lib'en uafhængig af auth.User.
    """
    ct = ContentType.objects.get_for_model(user.__class__)
    # understøt pk/id/uuid der kan castes til string
    return ct, str(getattr(user, 'pk', getattr(user, 'id', user)))


def _get_identifier(user) -> str:
    """Vælg label til otpauth:// — kan overrides via settings.TWOFACTOR_USER_LABEL_FIELD."""
    field = getattr(settings, 'TWOFACTOR_USER_LABEL_FIELD', None)
    if field:
        val = getattr(user, field, None)
        if val:
            return str(val)
    for attr in ('email', 'username', 'user_name', 'name'):
        val = getattr(user, attr, None)
        if val:
            return str(val)
    return str(getattr(user, 'pk', getattr(user, 'id', 'user')))


# ----- kerne-API (generic via GFK) -----

def create_or_get_2fa(user) -> UserTwoFactor:
    ct, oid = _ct_pk_for(user)
    obj = UserTwoFactor.objects.filter(content_type=ct, object_id=oid).first()
    if obj:
        return obj
    return UserTwoFactor.objects.create(content_type=ct, object_id=oid, secret_key=generate_secret_key())


def rotate_secret(user) -> UserTwoFactor:
    tf = create_or_get_2fa(user)
    tf.secret_key = generate_secret_key()
    tf.is_enabled = False  # kræver re-verifikation
    tf.save(update_fields=['secret_key', 'is_enabled'])
    return tf


def generate_secret_key() -> str:
    return pyotp.random_base32()


def build_provisioning_uri_for_user(user, secret_key: str, issuer: Optional[str] = None) -> str:
    issuer_name = issuer or getattr(settings, 'TWOFACTOR_ISSUER', 'TwoFactor')
    label = _get_identifier(user)
    return pyotp.TOTP(secret_key).provisioning_uri(name=label, issuer_name=issuer_name)


def build_provisioning_uri(user_label: str, secret_key: str, issuer: Optional[str] = None) -> str:
    issuer_name = issuer or getattr(settings, 'TWOFACTOR_ISSUER', 'TwoFactor')
    return pyotp.TOTP(secret_key).provisioning_uri(name=user_label, issuer_name=issuer_name)


def qr_png_bytes(provisioning_uri: str) -> bytes:
    img = qrcode.make(provisioning_uri).get_image()
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def qr_data_uri(provisioning_uri: str) -> str:
    return encode_data_uri('image/png', qr_png_bytes(provisioning_uri))


def verify_token(user, token: str, *, valid_window: int = 1) -> bool:
    """Verificér TOTP for en *enabled* bruger (generic user-model)."""
    ct, oid = _ct_pk_for(user)
    tf = UserTwoFactor.objects.filter(content_type=ct, object_id=oid, is_enabled=True).first()
    if not tf:
        return False
    totp = pyotp.TOTP(tf.secret_key)
    return totp.verify(str(token).strip(), valid_window=valid_window)


def enable_if_valid(user, token: str) -> bool:
    """Aktivér 2FA hvis koden matcher nuværende hemmelige nøgle (setup-step)."""
    tf = create_or_get_2fa(user)
    totp = pyotp.TOTP(tf.secret_key)
    if totp.verify(str(token).strip()):
        tf.is_enabled = True
        tf.save(update_fields=['is_enabled'])
        return True
    return False


# ----- backup-koder -----

def generate_backup_codes(user, *, amount: int = 10, token_bytes: int = 4) -> List[str]:
    """Generér engangskoder (hex). token_bytes=4 -> 8 hextegn per kode."""
    tf = create_or_get_2fa(user)
    codes: List[str] = []
    with transaction.atomic():
        for _ in range(amount):
            code = secrets.token_hex(token_bytes)
            BackupCode.objects.create(twofactor=tf, code=code)
            codes.append(code)
    return codes


def verify_backup_code(user, input_code: str) -> bool:
    ct, oid = _ct_pk_for(user)
    tf = UserTwoFactor.objects.filter(content_type=ct, object_id=oid).first()
    if not tf:
        return False
    try:
        bc = BackupCode.objects.get(twofactor=tf, code=str(input_code).strip(), used=False)
    except BackupCode.DoesNotExist:
        return False
    bc.used = True
    bc.save(update_fields=['used'])
    return True
