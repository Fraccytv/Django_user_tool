# 🔐 Django Modular User System

A modular, secure, and beginner-friendly user authentication system for Django – built completely without Django's default `auth.User`.

---

## 📦 Included Apps

### `accounts/`
- User registration
- Login / logout
- Password encryption using salt + `cryptography`
- Session-based authentication
- Custom forms using `forms.py`

### `log/`
- Tracks login attempts (success or failed)
- Stores IP address, timestamp, and event type
- Integrated with Django Admin (no frontend view required)

---

## 🧱 Project Structure

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
├── templates/
│ └── base.html
│
├── your_project/ ← Django project folder (settings.py, urls.py)
│
├── manage.py
└── requirements.txt

---

## 🚀 Getting Started

### 1. Copy the folders into your Django project

- Place `accounts/`, `log/`, and `templates/` in your main project.
- Make sure the directory structure matches the example above.

---

### 2. Update `settings.py`

Add both apps:

```python
INSTALLED_APPS = [
    ...,
    "accounts",
    "log",
]


3. Configure URLs
In your project-level urls.py, include the accounts app:


from django.urls import path, include

urlpatterns = [
    ...,
    path("", include("accounts.urls")),  # Login, register, logout, home
]
No need to include log/urls — the log app is handled via Django Admin.

4. Migrate the database
Run the following:


python manage.py makemigrations
python manage.py migrate

5. Create superuser (optional, for logs)
python manage.py createsuperuser
Then log into /admin to view login logs.

🔐 How It Works
When users register, their password is salted and encrypted using cryptography's Fernet.

On login, the password is decrypted and compared.

Sessions are used for authentication (not Django's default login system).

Login attempts are automatically logged in the log app.

🧪 Requirements
Python 3.8+

Django 4.x+

cryptography

Install dependencies:

pip install -r requirements.txt

💡 Ready for Expansion

This system is built to grow. Ideas for future apps:

profiles/ – custom user details, avatars, settings

twofactor/ – 2FA with QR and TOTP

auditlog/ – track changes and actions

sessiontracker/ – show active user sessions and device info

📝 License
MIT – free to use, modify, and share.

✍️ Author
Built with ❤️ by [Your Name]. Contributions welcome.