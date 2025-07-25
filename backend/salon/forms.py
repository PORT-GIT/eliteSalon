from django import forms
from .models import service, salonAppointment, servicesGiven
from users.models import EmployeeProfile

class ServiceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = ['category', 'service_name', 'price', 'description', 'durationOfService']


class AppointmentsForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=service.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    # this allows multiple selection of services
    scheduleDay = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    endTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = salonAppointment
        fields = ['services', 'employeeId', 'scheduleDay', 'appointmentStatus', 'startTime', 'endTime']
        
        # def __init__(self, *args, **kwargs):
        #     super(AppointmentsForm, self).__init__(*args, **kwargs)
        #     # We can customize the queryset for employees if needed, e.g., only active employees
        #     self.fields['employeeId'].queryset = employeeProfile.objects.filter(is_active=True)


class ServicesGivenForm(forms.ModelForm):
    class Meta:
        model = servicesGiven
        fields = ['salonAppointmentId', 'servicesId', 'customerId', 'employeeId', 'customerRating', 'customerRating', 'customerComment', 'employeeRating', 'employeeComment']
