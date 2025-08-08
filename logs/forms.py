# logs/forms.py
from django import forms
from .models import Log

class LogFilterForm(forms.Form):
    username = forms.CharField(required=False, label="User")
    ip = forms.GenericIPAddressField(required=False, label="IP")
    status = forms.ChoiceField(
        required=False, choices=[("", "All")] + Log.STATUS_CHOICES, label="Status"
    )
    event_type = forms.ChoiceField(
        required=False, choices=[("", "All")] + Log.EVENT_CHOICES, label="Event"
    )
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))