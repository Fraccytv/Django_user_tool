from django.urls import path
from . import views

urlpatterns = [
    path("2fa/activate/", views.activate_2fa, name="activate_2fa"),
]