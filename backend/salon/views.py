from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ServiceForm, ServicesGivenForm
from .models import service, salonAppointment, servicesGiven
from django.contrib.auth.decorators import login_required
# this imports will help in the view to calculate the time an appointment will take
import re
from datetime import datetime, timedelta
from formtools.wizard.views import SessionWizardView
from .appointment_form_wizard import SelectServicesForm, SelectDateForm, ConfirmDetailsForm
# this will help in the employee assignment to the appointment
from django.db.models import Count, Q
from users.models import EmployeeProfile

class ServicesGivenListView(ListView):
    model = servicesGiven
    template_name = 'salon/services_given.html'
    context_object_name = 'services-given'

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
            messages.success(request, 'Service saved successfully')
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
    dummy_date = datetime(2000, 1, 1, start_time.hour, start_time.minute, start_time.second)
    end_datetime = dummy_date + timedelta(minutes=duration_minutes)
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
    
    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step  == 'services':
            # this will ensure that the form is populated with the services available
            # it will also override the form's queryset to include all services
            form.fields['services'].queryset = service.objects.all()

        return form
    
    def done(self, form_list, **kwargs):
        # all the data from the forms will be processed here to create an appointment
        services_form = form_list[0]
        date_form = form_list[1]
        confirm_form = form_list[2]

        services = services_form.cleaned_data['services']
        schedule_day = date_form.cleaned_data['scheduleDay']
        appointment_time = confirm_form.cleaned_data['appointmentTime']

        # this section will handle the employee selection
        # this will assign employees who offer  at least on of the services selected by customer
        # this means that a user can be served by multiple employees
        service_ids = [service.id for service in services]
        employees = EmployeeProfile.objects.filter(
            services_to_offer__in=service_ids, work_status='FREE'
        ).distinct()

        # this will filter employees who are available on the selected schedule day and time
        # and it will check the existing appointments to avoid conflicts
        available_employees = []
        for employee in employees:
            conflicting_appointments = employee.salonappointment_set.filter(
                scheduleDay=schedule_day,
                appointmentTime=appointment_time
            )
            if not conflicting_appointments.exists():
                available_employees.append(employee)

        if not available_employees:
            messages.error(self.request, 'No available employees for the selected service and time')
            return redirect('homepage')
        
        # this will assign all available employees
        assigned_employees = available_employees


        # this will create the appointment for each assigned employee
        for assigned_employee in assigned_employees:

            total_duration = total_services_duration(services)
            appointment_end_time = calculate_end_time(appointment_time, total_duration)

            appointment = salonAppointment.objects.create(
                customerId=self.request.user.customer_profile,
                scheduleDay=schedule_day,
                appointmentTime=appointment_time,
                appointmentEndTime = appointment_end_time,
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
