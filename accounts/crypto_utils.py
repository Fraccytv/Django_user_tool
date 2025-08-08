import os
import base64
from hmac import compare_digest
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# hvorfor: irreversibel hash i stedet for dekrypterbar kryptering

ITERATIONS = 210_000  # kan hæves i prod


def generate_salt() -> bytes:
    return os.urandom(16)


def _derive(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return kdf.derive(password)


def hash_password(password: str, salt: bytes) -> str:
    if isinstance(password, str):
        password = password.encode()
    dk = _derive(password, salt)
    return base64.urlsafe_b64encode(dk).decode()


def verify_password(password: str, salt_b64: str, stored_hash_b64: str) -> bool:
    salt = base64.b64decode(salt_b64)
    calc = hash_password(password, salt)
    return compare_digest(calc, stored_hash_b64)