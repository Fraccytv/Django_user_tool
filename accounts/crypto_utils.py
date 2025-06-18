import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


def generate_salt():
    return os.urandom(16)


def generate_key(user_password, salt):
    if isinstance(user_password, str):
        user_password = user_password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(user_password))


def encrypt_password(raw_password, key):
    f = Fernet(key)
    return f.encrypt(raw_password.encode())


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()
