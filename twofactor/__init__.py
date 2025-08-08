# twofactor/__init__.py
"""
Drop-in backend-bibliotek til TOTP 2FA (uden views/urls/templates).

Brug altid:
    from twofactor.services import (
        create_or_get_2fa, rotate_secret, generate_secret_key,
        build_provisioning_uri, qr_data_uri, qr_png_bytes,
        verify_token, enable_if_valid, generate_backup_codes, verify_backup_code,
    )

Bevidst ingen imports her – undgår AppRegistryNotReady under django.setup().
"""
__all__ = [
    "create_or_get_2fa",
    "rotate_secret",
    "generate_secret_key",
    "build_provisioning_uri",
    "qr_data_uri",
    "qr_png_bytes",
    "verify_token",
    "enable_if_valid",
    "generate_backup_codes",
    "verify_backup_code",
]
