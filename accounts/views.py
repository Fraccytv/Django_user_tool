import base64

from django.shortcuts import render, redirect
from .crypto_utils import (
    generate_key,
    generate_salt,
    encrypt_password,
    decrypt_password,
)
from .models import User
from .forms import RegisterForm, LoginForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            errors = []

            # ✅ Password match check
            if password != confirm_password:
                errors.append("Passwords do not match.")

            # ✅ Tjek om brugernavn og email allerede er i brug
            if User.objects.filter(username=username).exists():
                errors.append("Username already in use.")
            if User.objects.filter(email=email).exists():
                errors.append("Email already in use.")

            if errors:
                return render(
                    request, "accounts/register.html", {"form": form, "errors": errors}
                )

            # ✅ Krypter adgangskode
            salt = generate_salt()
            key = generate_key(password, salt)
            encrypted_pw = encrypt_password(password, key)
            salt_str = base64.b64encode(salt).decode()

            # ✅ Opret bruger
            User.objects.create(
                username=username.lower(),  # bonus: normaliseret
                email=email.lower(),  # bonus: normaliseret
                encrypted_password=encrypted_pw.decode(),
                salt=salt_str,
            )

            # ✅ Redirect i stedet for render (undgår resubmit)
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username").lower()
        password = form.cleaned_data.get("password")

        try:
            user = User.objects.get(username=username)

            # ✅ Beskyt mod manglende data
            if not user.salt or not user.encrypted_password:
                return render(
                    request,
                    "accounts/login.html",
                    {
                        "form": form,
                        "error": "User data corrupted. Please reset or contact support.",
                    },
                )

            # ✅ Dekrypter adgangskode
            salt = base64.b64decode(user.salt.encode())
            key = generate_key(password, salt)
            decrypted_password = decrypt_password(user.encrypted_password.encode(), key)

            if decrypted_password == password:
                request.session["user_id"] = user.id
                return redirect("home")
            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "error": "Invalid credentials."},
                )

        except User.DoesNotExist:
            return render(
                request,
                "accounts/login.html",
                {"form": form, "error": "Invalid credentials."},
            )

    return render(request, "accounts/login.html", {"form": form})


def home(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")

    return render(request, "accounts/home.html", {"user": user})

def logout_view(request):
    if request.method == "POST":
        request.session.flush()
        return redirect("login")

    return render(request, "accounts/logout.html")
