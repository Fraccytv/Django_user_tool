from functools import wraps
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods


from .forms import LoginForm, RegisterForm
from .models import CustomUser
from logs.models import Log  

from urllib.parse import urlencode
from .helpers import get_safe_next_url

def session_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("user_id"):
            next_url = request.get_full_path()
            login_url = reverse("login")
            return redirect(f"{login_url}?{urlencode({'next': next_url})}")
        return view_func(request, *args, **kwargs)
    return _wrapped


def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            cd = form.cleaned_data
            if CustomUser.objects.filter(username=cd.get("username")).exists():
                form.add_error("username", "Username already in use.")
            if CustomUser.objects.filter(email=cd.get("email")).exists():
                form.add_error("email", "Email already in use.")
            if not form.errors:
                form.add_error(None, "Could not create user. Please try again.")
        else:
            # valgfri log
            try:
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user, ip_address=ip, status="success", event_type="register"
                )
            except Exception:
                pass
            return redirect("login")

    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            request.session.flush()
            request.session["user_id"] = user.id
            try:
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(user=user, ip_address=ip, status="success", event_type="login")
            except Exception:
                pass
            return redirect(get_safe_next_url(request))
        try:
            ip = request.META.get("REMOTE_ADDR", "unknown_ip")
            Log.objects.create(
                user=None,
                ip_address=ip,
                status="failure",
                event_type="login",
            )
        except Exception:
            pass
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
                Log.objects.create(
                    user=user, ip_address=ip, status="success", event_type="logout"
                )
            except CustomUser.DoesNotExist:
                pass
            except Exception:
                pass
        request.session.flush()
        return redirect("login")
    return render(request, "accounts/logout.html")
