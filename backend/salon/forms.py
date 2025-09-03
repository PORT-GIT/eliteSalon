from django import forms
from .models import service, salonAppointment, servicesGiven
from users.models import EmployeeProfile, CustomerProfile
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta

class ServiceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = ['category', 'service_name', 'price', 'description', 'durationOfService']

class AppointmentBookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select the services you want"
    )
    
    scheduleDay = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': date.today().strftime('%Y-%m-%d')
        }),
        required=True
    )
    
    appointmentTime = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        required=True
    )
    
    class Meta:
        model = salonAppointment
        fields = ['services', 'employeeId', 'scheduleDay', 'appointmentTime']
        widgets = {
            'employeeId': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        self.fields['employeeId'].queryset = EmployeeProfile.objects.filter(work_status='FREE')
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
                # Parse duration string (e.g., "1 hour 30 minutes")
                duration_str = service_obj.durationOfService
                duration_parts = duration_str.split()
                duration = timedelta()
                
                for i in range(0, len(duration_parts), 2):
                    if i + 1 < len(duration_parts):
                        value = int(duration_parts[i])
                        unit = duration_parts[i + 1]
                        if 'hour' in unit:
                            duration += timedelta(hours=value)
                        elif 'minute' in unit:
                            duration += timedelta(minutes=value)
                
                total_duration += duration
            
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
