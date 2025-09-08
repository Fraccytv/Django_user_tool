from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from .services import is_locked, register_failed_attempt, reset_attempts
from .services import generate_salt, hash_password, verify_password

# REGISTRATION FORM


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Confirm Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            username = username.lower().strip()
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError("Username already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower().strip()
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Email already in use.")
        return email

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords do not match.")
        if not cleaned.get("username") or not cleaned.get("email") or not pw:
            raise ValidationError("All fields are required.")
        return cleaned

    def save(self) -> CustomUser:
        """
        Opretter brugeren med én salt (samme salt til hashing og lagring).
        """
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        salt = generate_salt()
        encrypted_password = hash_password(password, salt)

        return CustomUser.objects.create(
            username=username,
            email=email,
            salt=salt,
            encrypted_password=encrypted_password,
        )


# LOGIN FORM


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"
            f.widget.attrs["placeholder"] = f.label
        self._user = None
        self.error_code = None  # "invalid", "locked", etc.

    def clean_username(self):
        u = self.cleaned_data.get("username")
        return u.lower().strip() if u else u

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")
        if not username or not password:
            self.error_code = "missing_fields"
            raise forms.ValidationError("Both fields are required.")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            self.error_code = "invalid"
            raise forms.ValidationError("Invalid.")

        if is_locked(user):
            self.error_code = "locked"
            raise forms.ValidationError("Invalid")

        if not verify_password(password, user.salt, user.encrypted_password):
            try:
                ip = self.data.get("ip_address")
            except Exception:
                ip = None
            register_failed_attempt(user, ip=ip)
            self.error_code = "invalid"
            raise forms.ValidationError("Invalid.")

        reset_attempts(user)
        self._user = user
        return cleaned

    def get_user(self):
        return self._user
