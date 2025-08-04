# Django Modular User System

A modular, secure, and beginner-friendly user authentication system for Django – built completely **without Django's default `auth.User`**.

---

## Included Apps

### `accounts/`
- User registration
- Login / logout
- Password encryption using salt + `cryptography`
- Session-based authentication (no `auth.User`)
- Custom forms using `forms.py`

### `log/`
- Tracks login attempts (success or failed)
- Stores IP address, timestamp, and event type
- Integrated with Django Admin (no frontend view required)

### `twofactor/`
- Optional TOTP-based two-factor authentication (2FA)
- Secret key generation using `pyotp`
- QR code generation using `qrcode`
- Token validation for user authentication
- Designed as a standalone library – no views or UI code

### `profiles/`
- Optional user profile extension
- Stores additional user info like name, avatar, and settings
- Linked to your custom user model via `OneToOneField`
- Easy to extend and customize

---

## Project Structure

your_project/
├── accounts/
│ ├── crypto_utils.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/accounts/
│ ├── login.html
│ ├── logout.html
│ ├── register.html
│ └── home.html
│
├── log/
│ ├── models.py
│ ├── admin.py
│
├── twofactor/
│ ├── models.py
│ ├── services.py
│ ├── utils.py
│
├── profiles/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/profiles/
│ └── profile.html
│
├── templates/
│ └── base.html
│
├── your_project/ # Django project folder (settings.py, urls.py)
│
├── manage.py
└── requirements.txt


---

## 🚀 Getting Started

### 1. Copy the folders into your Django project

- Place `accounts/`, `log/`, `twofactor/`, `profiles/`, and `templates/` in your main project folder.
- Make sure the directory structure matches the example above.

---

### 2. Update `settings.py`

Add all apps:

```python
INSTALLED_APPS = [
    ...,
    "accounts",
    "log",
    "twofactor",
    "profiles",
]


from django.urls import path, include

urlpatterns = [
    ...,
    path("", include("accounts.urls")),   # Login, register, logout, home
    path("profiles/", include("profiles.urls")),  # Optional profile pages
]

MIGRATE THE DATABASE
python manage.py makemigrations
python manage.py migrate


(OPTIONAL) Create superuser for Admin
python manage.py createsuperuser


How It Works
Passwords are encrypted using cryptography with salt per user.

Users log in via custom views and session logic – not Django's built-in login.

All login attempts are recorded via the log app.

The twofactor/ app can be optionally used to enable 2FA via TOTP.

The profiles/ app allows extra user info to be stored and edited.

How to Use the twofactor/ App
The twofactor/ app is designed as a library, not a full UI.

It gives you:

Secret key generation:

from twofactor.services import generate_secret_key
 QR code generation:


from twofactor.services import get_user_qr  # uses user.email + secret_key

Token verification:

from twofactor.services import verify_token

if verify_token(user, token):
    user.usertwofactor.is_enabled = True
    user.usertwofactor.save()

You build your own forms and templates to scan, activate, and verify tokens.

🧪 Requirements
Python 3.8+

Django 4.x+

cryptography

pyotp

qrcode

Pillow (for QR image generation)

Install dependencies:
pip install -r requirements.txt

Built for Expansion
This system is built to grow with you.

Ideas for future apps:

auditlog/ – track user actions, model edits

sessiontracker/ – view active sessions, devices, and locations

License
MIT – free to use, modify, and share.

Author
by Kennet Olesen – Fraccy
Contributions welcome!