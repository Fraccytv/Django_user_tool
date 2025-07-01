from django.urls import path
from . import views

urlpatterns = [
    path("logs/", views.login_log_list, name="log_list"),
]