from django.urls import path
from . import views

urlpatterns = [
    # Profile view
    path("profile/", views.profile_view, name="profile_view"),
    # Profile edit
    path("profile/edit/", views.edit_profile, name="profile_edit"),
]
