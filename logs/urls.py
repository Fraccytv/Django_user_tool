# logs/urls.py
from django.urls import path
from .views import login_log_list

app_name = "logs"

urlpatterns = [
    path("logs/", login_log_list, name="log_list"),  # ender som /logs/ når inkluderet fra ""
]