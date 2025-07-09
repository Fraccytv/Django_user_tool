from accounts.models import CustomUser
from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Your location'}),
            # 'birth_date': forms.DateInput(attrs={'type': 'date'}),
            # 'profile_picture': forms.ClearableFileInput(),
        }