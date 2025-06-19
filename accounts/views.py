import base64

from django.shortcuts import render, redirect
from .crypto_utils import (
    generate_key,
    generate_salt,
    encrypt_password,
    decrypt_password,
)
from .models import User
from .forms import RegisterForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            
        
            errors = []
            if User.objects.filter(username=username).exists():
                errors.append("Already in use.")
            if User.objects.filter(email=email).exists():
                errors.append("Already in use.")

            if errors:
                return render(request, "accounts/register.html", {"form": form, "errors": errors})


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
        
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    return render(request, "accounts/login.html")