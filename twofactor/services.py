import pyotp
import qrcode
from io import BytesIO
from .models import UserTwoFactor
import base64

def verify_token(user, token):
    try:
        tf = user.usertwofactor
        if not tf.is_enabled:
            return False
        totp = pyotp.TOTP(tf.secret_key)
        return totp.verify(token)
    except UserTwoFactor.DoesNotExist:
        return False


def generate_secret_key():
    return pyotp.random_base32()

def generate_provisioning_uri(user_email, secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.provisioning_uri(name=user_email, issuer_name='Django_user_tools_twofactor')

def generate_qr_code(uri):
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

def get_user_qr(user_email, secret_key):
    uri = generate_provisioning_uri(user_email, secret_key)
    return generate_qr_code(uri)