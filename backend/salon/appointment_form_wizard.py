from django import forms
from .models import service
from users.models import EmployeeProfile

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

class EmployeeSelectionForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=EmployeeProfile.objects.none(),
        required=True,
        label="Select Employee"
    )

    def __init__(self, *args, **kwargs):
        employee_queryset = kwargs.pop('employee_queryset', None)
        super().__init__(*args, **kwargs)
        if employee_queryset is not None:
            self.fields['employee'].queryset = employee_queryset

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




