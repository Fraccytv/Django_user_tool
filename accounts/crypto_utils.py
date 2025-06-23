import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

# Generate a random salt (used to create unique encryption keys)
def generate_salt():
    return os.urandom(16)

# Create a key from a user's password and salt
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

# Encrypt password (or any text) with the given key
def encrypt_password(raw_password, key):
    f = Fernet(key)
    return f.encrypt(raw_password.encode())

# Decrypt the password using the same key
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()
