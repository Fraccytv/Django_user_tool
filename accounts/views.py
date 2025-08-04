import base64

from django.shortcuts import render, redirect
from .crypto_utils import ( generate_key, generate_salt, encrypt_password, decrypt_password,
)
from .models import CustomUser  
from .forms import RegisterForm, LoginForm  
from logs.models import Log
from utils.decorators import session_login_required 
# from twofactor.backup import verify_backup_code





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

            #  Check if passwords match
            if password != confirm_password:
                errors.append("Passwords do not match.")

            #  Check for duplicate username or email
            if CustomUser.objects.filter(username=username).exists():
                errors.append("Username already in use.")
            if CustomUser.objects.filter(email=email).exists():
                errors.append("Email already in use.")

            if errors:
                return render(
                    request,
                    "accounts/register.html",  #  CHANGE if your templates folder is renamed
                    {"form": form, "errors": errors},
                )

            #  Encrypt password before saving
            salt = generate_salt()
            key = generate_key(password, salt)
            encrypted_pw = encrypt_password(password, key)
            salt_str = base64.b64encode(salt).decode()

            #  Create user and store instance in a variable
            user = CustomUser.objects.create(
                username=username.lower() if username else "",
                email=email.lower() if email else "",
                encrypted_password=encrypted_pw.decode(),
                salt=salt_str,
            )

            #  Use the actual user object for logging
            ip = request.META.get("REMOTE_ADDR", "unknown_ip")
            Log.objects.create(
                user=user,  # ← not User (the class), not a string. The instance you just created
                ip_address=ip,
                status="success",
                event_type="register",  # Optional: Use "register" instead of "login"
            )

            return redirect("login")  #  CHANGE if your login URL name is different

    else:
        form = RegisterForm()

    return render(
        request, "accounts/register.html", {"form": form}
    )  #  CHANGE if needed


# ==========================
# LOGIN
# ==========================
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        if username:
            username = username.lower()
        else:
            username = ""
        password = form.cleaned_data.get("password")

        try:
            user = CustomUser.objects.get(username=username)

            #  Protect against corrupted user data
            if not user.salt or not user.encrypted_password:
                return render(
                    request,
                    "accounts/login.html",  #  CHANGE if needed
                    {
                        "form": form,
                        "error": "User data corrupted. Please reset or contact support.",
                    },
                )

            #  Decrypt password and compare
            salt = base64.b64decode(user.salt.encode())
            key = generate_key(password, salt)
            decrypted_password = decrypt_password(user.encrypted_password.encode(), key)

            if decrypted_password == password:
                request.session["user_id"] = user.id  #  Store user in session

                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user,
                    ip_address=ip,
                    status="success",
                    event_type="login",
                )

                return redirect("home")  #  CHANGE if your home URL name is different

                # ================================================
                # BACKUP CODE FALLBACK (2FA bypass if needed)
                # ================================================
                # from twofactor.backup import verify_backup_code
                #
                # code_input = request.POST.get("backup_code")
                #
                # if verify_backup_code(user, code_input):
                #     login(request, user)  # Django login
                #     return redirect("dashboard")
                # else:
                #     return render(
                #         request,
                #         "twofactor/verify_2fa.html",
                #         {"error": "Invalid backup code"},
                #     )
                # ================================================

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

        except CustomUser.DoesNotExist:
            return render(
                request,
                "accounts/login.html",
                {"form": form, "error": "Invalid credentials."},
            )

    return render(request, "accounts/login.html", {"form": form})  #  CHANGE if needed



# ==========================
# HOME (Protected View)
# ==========================
@session_login_required  
def home(request):
    user_id = request.session.get("user_id")
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect("login")

    return render(request, "accounts/home.html", {"user": user})  #  CHANGE if needed


# ==========================
# LOGOUT
# ==========================
def logout_view(request):

    if request.method == "POST":
        # 🔥 Clear the session to log out the use
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                ip = request.META.get("REMOTE_ADDR", "unknown_ip")
                Log.objects.create(
                    user=user,
                    ip_address=ip,
                    status="success",
                    event_type="logout",
                )
            except CustomUser.DoesNotExist:
                pass
        request.session.flush()  # 🔥 Completely clears the session (logs out user)
        return redirect("login")  # ⚠️ CHANGE if your login view name is different

    return render(request, "accounts/logout.html")  # ⚠️ CHANGE if needed
