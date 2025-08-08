from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell us about yourself...", "class": "form-control"}),
            "location": forms.TextInput(attrs={"placeholder": "Your location", "class": "form-control"}),
        }