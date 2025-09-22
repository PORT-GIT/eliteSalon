from django import forms
from .models import service, salonAppointment, servicesGiven
from users.models import EmployeeProfile, CustomerProfile
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta

class ServiceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = ['category', 'service_name', 'price', 'description', 'new_durationOfService']

class AppointmentBookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Services",
        help_text="Select the services you want"
    )

    scheduleDay = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': date.today().strftime('%Y-%m-%d')
        }),
        required=True,
        label="Appointment Date"
    )

    appointmentTime = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        required=True,
        label="Appointment Time"
    )

    class Meta:
        model = salonAppointment
        fields = ['services', 'employeeId', 'scheduleDay', 'appointmentTime']
        widgets = {
            'employeeId': forms.Select(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        # this will calculate the total price of services before services
        services = self.cleaned_data.get('services', [])
        total_price = sum(service.price for service in services)

        # this will create the appointment instance
        appointment = super().save(commit=False)
        appointment.total_price = total_price

        if commit:
            appointment.save()
            self.save_m2m() #this will save the many to many relationships that i considered when selecting multiple services

        return appointment

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        self.fields['employeeId'].queryset = EmployeeProfile.objects.all()
        self.fields['employeeId'].label = "Select Stylist"

    def clean(self):
        cleaned_data = super().clean()
        schedule_day = cleaned_data.get('scheduleDay')
        appointment_time = cleaned_data.get('appointmentTime')
        employee = cleaned_data.get('employeeId')
        services = cleaned_data.get('services')

        if schedule_day and appointment_time and employee and services:
            # Check if the time slot is available
            appointment_datetime = datetime.combine(schedule_day, appointment_time)

            # Calculate total duration
            total_duration = timedelta()
            for service_obj in services:
                total_duration += service_obj.new_durationOfService

            # Check for conflicting appointments
            end_time = appointment_datetime + total_duration

            conflicts = salonAppointment.objects.filter(
                employeeId=employee,
                scheduleDay=schedule_day,
                appointmentTime__lt=end_time.time(),
                appointmentEndTime__gt=appointment_time
            )

            if conflicts.exists():
                raise ValidationError(
                    "This time slot is already booked. Please choose another time."
                )

        return cleaned_data

class ServicesGivenForm(forms.ModelForm):
    class Meta:
        model = servicesGiven
        fields = ['salonAppointmentId', 'servicesId', 'customerId', 'employeeId',
                 'customerRating', 'customerComment', 'employeeRating', 'employeeComment']
        widgets = {
            'salonAppointmentId': forms.HiddenInput(),
            'servicesId': forms.HiddenInput(),
            'customerId': forms.HiddenInput(),
            'employeeId': forms.HiddenInput(),
            'customerRating': forms.Select(attrs={'class': 'form-control'}),
            'customerComment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'employeeRating': forms.Select(attrs={'class': 'form-control'}),
            'employeeComment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
