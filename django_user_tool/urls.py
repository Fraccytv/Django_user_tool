from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),           # /login, /register, /home
    path("logs/", include("logs.urls")),         # /logs/
    path("profiles/", include("profiles.urls")),  # /profiles/
]