from django import forms
from .models import service

class SelectServicesForm(forms.Form):
    service