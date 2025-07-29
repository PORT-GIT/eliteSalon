from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ServiceForm, ServicesGivenForm
from .models import service, salonAppointment, servicesGiven
from django.contrib.auth.decorators import login_required
from django import forms
# this imports will help in the view to calculate the time an appointment will take
import re
from datetime import time, datetime, timedelta
from formtools.wizard.views import SessionWizardView
from .appointment_form_wizard import SelectServicesForm, SelectDateForm, ConfirmDetailsForm, EmployeeSelectionForm
# this will help in the employee assignment to the appointment
from django.db.models import Count, Q
from users.models import EmployeeProfile
from django.db import transaction
from django.utils import timezone

class ServicesGivenListView(ListView):
    model = servicesGiven
    template_name = 'salon/services_given.html'
    context_object_name = 'services_given'

    def get_queryset(self):
        return servicesGiven.objects.all()
    
class ServicesListView(ListView):
    model = service
    template_name = 'salon/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return service.objects.all()

class AppointmentsListView(ListView):
    model = salonAppointment
    template_name = 'salon/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return salonAppointment.objects.all()
    
class AppointmentDetailView(DetailView):
    model = salonAppointment
    template_name = 'salon/appointment_detail.html'

class AppointmentDeleteView(DeleteView):
    model = salonAppointment
    template_name = 'salon/delete_appointment.html'
    success_url = reverse_lazy('appointments')
    # this will redirect me to the appointments page after deletion

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Appointment was deleted successfully')
        return super().delete(request, *args, **kwargs)
    
def create_services(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
            # the redirect should match the view class

    else:
        form = ServiceForm()
        messages.success(request, 'Service has not been saved successfully')
    
    return render(request, 'salon/add_services.html', {'form': form})

def parse_duration(duration_str):
    # this function will parse the duration string and return a timedelta object
    # this means that the time will be converted to mins sa that it can be calculated 
    duration_str = duration_str.lower()
    minutes = 0
    hour_match = re.search(r'(\d+)\s*hour', duration_str)
    minute_match = re.search(r'(\d+)\s*minute', duration_str)
    if hour_match:
        minutes += int(hour_match.group(1)) * 60
    
    if minute_match:
        minutes += int(minute_match.group(1))

    if not hour_match and not minute_match:
        try:
            minutes = int(duration_str)

        except ValueError:
            minutes = 0
    return minutes

# this calculated the total time of the selected services
def total_services_duration(services):
    total_minutes = 0
    for service in services:
        total_minutes += parse_duration(service.durationOfService)

    return total_minutes

# this function determines the endtime of the appointment based on the start time and the duration of service
def calculate_end_time(start_time, duration_minutes):
    # this function will calculate the end time of an appointment given the start time and duration in minutes
    # Combine with today's date using timezone
    now = timezone.now()
    start_datetime = timezone.make_aware(
        datetime.combine(now.date(), start_time)
    )
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)
    return end_datetime.time()

FORMS = [
    ("select_services", SelectServicesForm),
    ("select_date", SelectDateForm),
    ("confirm", ConfirmDetailsForm),
]

TEMPLATES = [
    ("select_services", "salon/select_services.html"),
    ("select_date", "salon/select_date.html"),
    ("confirm" , "salon/confirm_details.html"),
]

class AppointmentWizard(SessionWizardView):
    form_list = FORMS

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'select_services':
            # this will group services by category that will be passed to the services selection part of the appointment creation process
            services = service.objects.all().order_by('category', 'service_name')
            grouped_services = {}
            for svc in services:
                grouped_services.setdefault(svc.category, []).append(svc)
            context.update({'grouped_services': grouped_services})
        return context
    
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step == 'select_services':
            form.fields['services'].queryset = service.objects.all()
        elif step == 'confirm':
            cleaned_data = self.get_cleaned_data_for_step('select_date') or {}
            schedule_day = cleaned_data.get('scheduleDay')
            if schedule_day:
                available_times = self.get_available_times_slots(schedule_day)
                form.fields['appointmentTime'] = forms.ChoiceField(
                    choices=[(t.strftime("%H:%M"), t.strftime("%I:%M %p")) for t in available_times],
                    label="Select Appointment Time"
                )
        return form
    
    def get_available_times_slots(self, schedule_day):
        # i want to define the working hours of the salon
        start_work = time(9, 0) 
        # this means that work hours start at 9.00AM
        end_work = time(17, 0)
        # this means that work hours end at 5.00PM
        slot_duration = 30
        # each slot gets 30 minutes

        # this will get all appointments for the selected day
        appointments = salonAppointment.objects.filter(scheduleDay = schedule_day)

        # it will compute booking time ranges
        booked_ranges = []
        for appt in appointments:
            start = datetime.combine(schedule_day, appt.appointmentTime)
            end = datetime.combine(schedule_day, appt.appointmentEndTime)
            
            booked_ranges.append((start, end))

        # this function will generate all available slots
        slots = []
        current = datetime.combine(schedule_day, start_work)
        end = datetime.combine(schedule_day, end_work)
        while current + timedelta(minutes=slot_duration) <= end:
            # this will check if there is an appointment in this slot
            slots.append(current.time())
            current += timedelta(minutes=slot_duration)    

        # this will filter out the slots that are already taken by appointments
        free_slots = []
        for slot in slots:
            slot_start = datetime.combine(schedule_day, slot)
            slot_end = slot_start + timedelta(minutes=slot_duration)

            # this will check if slots overlap over booked time ranges
            
            if not any (slot_start < end and slot_end > start for start, end in booked_ranges):
                
                free_slots.append(slot)
        
        return free_slots
            

    def done(self, form_list, **kwargs):
        with transaction.atomic():
            # this will ensure that all the forms are valid before proceeding    
         # all the data from the forms will be processed here to create an appointment
            services_form = form_list[0]
            date_form = form_list[1]
            confirm_form = form_list[2]

            services = services_form.cleaned_data['services']
            schedule_day = date_form.cleaned_data['scheduleDay']
            appointment_time_str = confirm_form.cleaned_data['appointmentTime']
            appointment_time = datetime.strptime(appointment_time_str, "%H:%M").time()

            # Find an available employee who offers the selected service categories and is free at the appointment time
            categories = set(svc.category for svc in services)
            employees = EmployeeProfile.objects.filter(
                services_to_offer__category__in=categories,
                work_status='FREE'
            ).distinct()

            assigned_employee = None
            for employee in employees:
                conflicting_appointments = employee.salonappointment_set.filter(
                    scheduleDay=schedule_day,
                    appointmentTime__lt=calculate_end_time(appointment_time, total_services_duration(services)),
                    appointmentEndTime__gt=appointment_time
                )
                if not conflicting_appointments.exists():
                    assigned_employee = employee
                    break

            if not assigned_employee:
                messages.error(self.request, 'No available employee found for the selected services and time.')
                return redirect('homepage')

            total_duration = total_services_duration(services)
            appointment_end_time = calculate_end_time(appointment_time, total_duration)

            # Create the appointment
            appointment = salonAppointment.objects.create(
                customerId=self.request.user.customer_profile,
                scheduleDay=schedule_day,
                appointmentTime=appointment_time,
                appointmentEndTime=appointment_end_time,
                employeeId=assigned_employee,
                appointmentStatus='PENDING'
            )
            appointment.services.set(services)
            appointment.save()

            messages.success(self.request, 'Appointment was created successfully')
            return redirect('appointments')


def create_services_given(request):
    if request.method == 'POST':
        form = ServicesGivenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service given has been saved successfully')
            return redirect('add-services-given')
            # the redirect should match the view class
        
    else:
        form = ServicesGivenForm()
        messages.success(request, 'Service given has not been saved successfully')

    
    return render(request, 'salon/add_services_given.html', {'form': form})




#to consider the fact that a user won't need to enter their own details i can add the decorator below which will capture their details:
# @login_required
# def create_appointments(request):
#     if request.method == 'POST':
#         form = AppointmentsForm(request.POST)
#         if form.is_valid():
#             # the changes made here and to the form will ensure that the user does not
#             # select their details manually
#             # instead, the user will be captured automatically
#             # it also assigns the logged in user's profile to the appointment model customerID field
#             appointment = form.save(commit=False)
#             appointment.customerId = request.user.customer_profile
#             # customer_profile is added because the user is linked to the customer profile and not the 
#             # DJANGO USER model

#             services = form.cleaned_data['services']
#             total_duration = total_services_duration(services)

#             appointment_time = form.cleaned_data['appointmentTime']
#             appointment.appointmentEndTime = calculate_end_time(appointment_time, total_duration)

#             appointment.save()
#             form.save_m2m()# this will cater to saving the many services that can be selected
#             messages.success(request, 'Appointment saved successfully')
#             return redirect('appointments')
#             # the redirect should match the view class
#         else:
#             messages.error(request, 'Please correct the errors below')
#     else:
#         form = AppointmentsForm()
        
#     return render(request, 'salon/add_appointments.html', {'form': form})
