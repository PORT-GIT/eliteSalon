from django import forms
from .models import service, salonAppointment, servicesGiven

class ServiceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = ['category', 'service_name', 'price', 'description', 'durationOfService']


class AppointmentsForm(forms.ModelForm):
    class Meta:
        model = salonAppointment
        fields = ['customerId', 'services', 'employeeId', 'scheduleDay', 'appointmentStatus', 'startTime', 'endTime']


class ServicesGivenForm(forms.ModelForm):
    class Meta:
        model = servicesGiven
        fields = ['salonAppointmentId', 'servicesId', 'customerId', 'employeeId', 'customerRating', 'customerRating', 'customerComment', 'employeeRating', 'employeeComment']
