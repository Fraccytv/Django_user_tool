import base64

from django.shortcuts import render, redirect
from .crypto_utils import (  # Make sure this file is included in your new app
    generate_key,
    generate_salt,
    encrypt_password,
    decrypt_password,
)
from .models import User  # Your custom user model
from .forms import RegisterForm, LoginForm  # Make sure your forms.py is copied as well
from logs.models import Log



# ==========================
# REGISTER
# ==========================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            errors = []

            # 🔐 Check if passwords match
            if password != confirm_password:
                errors.append("Passwords do not match.")

            # 🧠 Check for duplicate username or email
            if User.objects.filter(username=username).exists():
                errors.append("Username already in use.")
            if User.objects.filter(email=email).exists():
                errors.append("Email already in use.")

            if errors:
                return render(
                    request,
                    "accounts/register.html",  # ⚠️ CHANGE if your templates folder is renamed
                    {"form": form, "errors": errors},
                )

            # 🔐 Encrypt password before saving
            salt = generate_salt()
            key = generate_key(password, salt)
            encrypted_pw = encrypt_password(password, key)
            salt_str = base64.b64encode(salt).decode()

            # ✅ Save user
            User.objects.create(
                username=username.lower(),  # Normalize input
                email=email.lower(),
                encrypted_password=encrypted_pw.decode(),
                salt=salt_str,
            )
            
            ip = request.META.get("REMOTE_ADDR", "unknown_ip")
            Log.objects.create(
                user=username,
                ip_address=ip,
                status="success",
                event_type="login",
            )

            return redirect("login")  # ⚠️ CHANGE if your login URL name is different

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})  # ⚠️ CHANGE if needed


# ==========================
# LOGIN
# ==========================
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username").lower()
        password = form.cleaned_data.get("password")

        try:
            user = User.objects.get(username=username)

            # ⚠️ Protect against corrupted user data
            if not user.salt or not user.encrypted_password:
                return render(
                    request,
                    "accounts/login.html",  # ⚠️ CHANGE if needed
                    {
                        "form": form,
                        "error": "User data corrupted. Please reset or contact support.",
                    },
                )

            # 🔓 Decrypt password and compare
            salt = base64.b64decode(user.salt.encode())
            key = generate_key(password, salt)
            decrypted_password = decrypt_password(user.encrypted_password.encode(), key)

            if decrypted_password == password:
                request.session["user_id"] = user.id  # ✅ Store user in session
                
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user,
                    ip_address=ip,
                    status="success",
                    event_type="login",
                )
                
                return redirect("home")  # ⚠️ CHANGE if your home URL name is different
            else:
                
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user,
                    ip_address=ip,
                    status="failure",
                    event_type="login",
                )
                
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

    return render(request, "accounts/login.html", {"form": form})  # ⚠️ CHANGE if needed


# ==========================
# HOME (Protected View)
# ==========================
def home(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")  # ⚠️ CHANGE if your login view name is different

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")

    return render(request, "accounts/home.html", {"user": user})  # ⚠️ CHANGE if needed


# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    
    if request.method == "POST":
        # 🔥 Clear the session to log out the use
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user.username,
                    ip_address=ip,
                    status="success",
                    event_type="logout",
                )
            except User.DoesNotExist:
                pass
        request.session.flush()  # 🔥 Completely clears the session (logs out user)
        return redirect("login")  # ⚠️ CHANGE if your login view name is different

    return render(request, "accounts/logout.html")  # ⚠️ CHANGE if needed
