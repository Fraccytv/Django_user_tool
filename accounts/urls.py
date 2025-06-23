from django.urls import path
from . import views

urlpatterns = [
    # Home page (after login)
    path("home/", views.home, name="home"),

    # User registration
    path("register/", views.register, name="register"),

    # User login
    path("login/", views.login_view, name="login"),

    # User logout (POST method expected)
    path("logout/", views.logout_view, name="logout"),
]

# 🔁 You can import this in your main project’s urls.py like:
# path("accounts/", include("yourapp.urls"))
