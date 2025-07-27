from django import forms
from .models import service

class SelectServicesForm(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Services"
    )

class SelectDateForm(forms.Form):
    scheduleDay = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        label="Select Date"
    )

class ConfirmDetailsForm(forms.Form):
    appointmentTime = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label="Select Appointment Time"
    )
    confirm = forms.BooleanField(
        required=True,
        label="I confirm the appointments details are correct"
    )