from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/edit/", views.edit_profile, name="profile_edit"),
]