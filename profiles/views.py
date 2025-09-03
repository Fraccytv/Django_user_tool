from django.shortcuts import render, redirect
from django.urls import reverse
from utils.decorators import session_login_required
from accounts.models import CustomUser
from .models import Profile
from .forms import ProfileForm

@session_login_required
def profile_view(request):
    user_id = request.session.get("user_id")
    user = CustomUser.objects.get(id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)
    return render(request, "profiles/profile.html", {"user": user, "profile": profile})

@session_login_required
def edit_profile(request):
    user_id = request.session.get("user_id")
    user = CustomUser.objects.get(id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form, "user": user, "profile": profile})