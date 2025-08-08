import base64
from django.shortcuts import render, redirect
from .crypto_utils import generate_salt, hash_password, verify_password
from .models import CustomUser
from .forms import RegisterForm, LoginForm
from logs.models import Log
from utils.decorators import session_login_required


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username", "").lower()
            email = form.cleaned_data.get("email", "").lower()
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            errors = []
            if password != confirm_password:
                errors.append("Passwords do not match.")
            if CustomUser.objects.filter(username=username).exists():
                errors.append("Username already in use.")
            if CustomUser.objects.filter(email=email).exists():
                errors.append("Email already in use.")

            if errors:
                return render(request, "accounts/register.html", {"form": form, "errors": errors})

            salt = generate_salt()
            salt_b64 = base64.b64encode(salt).decode()
            pw_hash = hash_password(password, salt)

            user = CustomUser.objects.create(
                username=username,
                email=email,
                encrypted_password=pw_hash,  # felt genbrugt som hash
                salt=salt_b64,
            )

            ip = request.META.get("REMOTE_ADDR", "unknown_ip")
            Log.objects.create(user=user, ip_address=ip, status="success", event_type="register")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = (form.cleaned_data.get("username") or "").lower()
        password = form.cleaned_data.get("password")
        try:
            user = CustomUser.objects.get(username=username)
            if not user.salt or not user.encrypted_password:
                return render(request, "accounts/login.html", {"form": form, "error": "User data corrupted. Please reset or contact support."})

            if verify_password(password, user.salt, user.encrypted_password):
                request.session["user_id"] = user.id
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(user=user, ip_address=ip, status="success", event_type="login")
                return redirect("home")
            else:
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(user=user, ip_address=ip, status="failure", event_type="login")
                return render(request, "accounts/login.html", {"form": form, "error": "Invalid credentials."})
        except CustomUser.DoesNotExist:
            return render(request, "accounts/login.html", {"form": form, "error": "Invalid credentials."})
    return render(request, "accounts/login.html", {"form": form})


@session_login_required
def home(request):
    user_id = request.session.get("user_id")
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect("login")
    return render(request, "accounts/home.html", {"user": user})


def logout_view(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(user=user, ip_address=ip, status="success", event_type="logout")
            except CustomUser.DoesNotExist:
                pass
        request.session.flush()  # why: session fixation mitigation
        return redirect("login")
    return render(request, "accounts/logout.html")