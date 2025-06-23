from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Confirm Password"
    )
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
        
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Password"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label