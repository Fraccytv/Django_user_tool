import base64

from django.shortcuts import render
from .crypto_utils import (
    generate_key,
    generate_salt,
    encrypt_password,
    decrypt_password,
)
from .models import User

# Create your views here.


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if username and password and email:
            errors = []
            if User.objects.filter(username=username).exists():
                errors.append("Already in use.")
            if User.objects.filter(email=email).exists():
                errors.append("Already in use.")

            if errors:
                return render(request, "accounts/register.html", {"errors": errors})

            salt = generate_salt()
            key = generate_key(password, salt)
            encrypted_pw = encrypt_password(password, key)

            salt_str = base64.b64encode(salt).decode()

            User.objects.create(
                username=username,
                email=email,
                encrypted_password=encrypted_pw.decode(),
                salt=salt_str,
            )

            return render(request, "accounts/login.html")

    return render(request, "accounts/register.html")
