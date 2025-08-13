# Django Modular User System

A modular, secure, and beginner-friendly user authentication system for Django – built completely **without Django's default `auth.User`**.

---

## Included Apps (Drag & Drop Ready)

### `accounts/`

* User registration & login/logout
* Password encryption using salt + `cryptography`
* Session-based authentication (no `auth.User`)
* Bootstrap-ready forms in `forms.py`

### `logs/`

* Tracks **all** events (login, logout, register, etc.)
* Stores IP, timestamp, event type, and status
* Admin interface for filtering/searching

### `twofactor/`

* Optional TOTP-based two-factor authentication (2FA)
* Secret key generation with `pyotp`
* QR code creation with `qrcode`
* Token validation logic
* Backend library only (no views/templates).

### `profiles/`

* Optional user profile extension
* Stores bio, location, and other user info
* Linked to `CustomUser` via `OneToOneField`
* Auto-created on user registration via Django signals

---

## Project Structure

```
your_project/
├── accounts/
├── logs/
├── twofactor/
├── profiles/
├── templates/
├── your_project/
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Copy these folders into your Django project

`accounts/`, `logs/`, `twofactor/`, `profiles/`, and `templates/`

### 3. Update `settings.py`

```
INSTALLED_APPS = [
    ...,
    'bootstrap5',
    'accounts',
    'logs',
    'twofactor',
    'profiles',
]
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
```

### 4. Update `urls.py`

```
urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('logs.urls')),
    path('profiles/', include('profiles.urls')),
]
```

### 5. Migrate database

```
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optional) Create admin user

```
python manage.py createsuperuser
```

---

## How It Works

* Passwords are encrypted with a unique salt per user.
* Login/logout handled with custom session logic.
* `logs/` tracks every important action.
* `twofactor/` can be used to add TOTP-based 2FA.
* `profiles/` extends user info.

---

## Future Ideas


---

## License

MIT – free to use and modify.

**Author:** Fraccy
# Django Modular User System

A modular, secure, and beginner-friendly user authentication system for Django – built completely **without Django's default `auth.User`**.

---

## Included Apps (Drag & Drop Ready)

### `accounts/`

* User registration & login/logout
* Password encryption using salt + `cryptography`
* Session-based authentication (no `auth.User`)
* Bootstrap-ready forms in `forms.py`

### `logs/`

* Tracks **all** events (login, logout, register, etc.)
* Stores IP, timestamp, event type, and status
* Admin interface for filtering/searching

### `twofactor/`

* Optional TOTP-based two-factor authentication (2FA)
* Secret key generation with `pyotp`
* QR code creation with `qrcode`
* Token validation logic
* Backend library only (no views/templates).

### `profiles/`

* Optional user profile extension
* Stores bio, location, and other user info
* Linked to `CustomUser` via `OneToOneField`
* Auto-created on user registration via Django signals

---

## Project Structure

```
your_project/
├── accounts/
├── logs/
├── twofactor/
├── profiles/
├── templates/
├── your_project/
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Copy these folders into your Django project

`accounts/`, `logs/`, `twofactor/`, `profiles/`, and `templates/`

### 3. Update `settings.py`

```
INSTALLED_APPS = [
    ...,
    'bootstrap5',
    'accounts',
    'logs',
    'twofactor',
    'profiles',
]
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
```

### 4. Update `urls.py`

```
urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('logs.urls')),
    path('profiles/', include('profiles.urls')),
]
```

### 5. Migrate database

```
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optional) Create admin user

```
python manage.py createsuperuser
```

---

## How It Works

* Passwords are encrypted with a unique salt per user.
* Login/logout handled with custom session logic.
* `logs/` tracks every important action.
* `twofactor/` can be used to add TOTP-based 2FA.
* `profiles/` extends user info.

---

## Future Ideas


---

## License

MIT – free to use and modify.

**Author:** Fraccy
