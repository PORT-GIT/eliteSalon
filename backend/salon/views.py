from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ServiceForm, ServicesGivenForm, AppointmentBookingForm
from .models import service, salonAppointment, servicesGiven
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# this imports will help in the view to calculate the time an appointment will take
import re
from datetime import time, datetime, timedelta
from formtools.wizard.views import SessionWizardView
# this will help in the employee assignment to the appointment
from django.db.models import Count, Q
from users.models import EmployeeProfile, CustomerProfile
from django.db import transaction
from django.utils import timezone
from django.core.serializers import serialize
import json

class ServicesGivenListView(ListView):
    model = servicesGiven
    template_name = 'salon/services_given.html'
    context_object_name = 'services_given'

    def get_queryset(self):
        return servicesGiven.objects.all()
    
def list_of_services(request):

    return render(request, 'salon/services_list.html')

def about_us(request):

    return render(request, 'salon/about-us.html')


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

def booking_calendar(request):
    """Display the interactive booking calendar"""
    services = service.objects.all()
    employees = EmployeeProfile.objects.all()  # Remove is_active filter
    
    context = {
        'services': services,
        'employees': employees,
    }
    return render(request, 'salon/booking_calendar.html', context)

@login_required
def book_appointment_ajax(request):
    """Handle appointment booking via AJAX"""
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, customer=request.user.customer_profile)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    appointment = form.save(commit=False)
                    appointment.customerId = request.user.customer_profile
                    
                    # Calculate end time based on services
                    services = form.cleaned_data['services']
                    total_duration = timedelta()
                    
                    for service_obj in services:
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
                    
                    # Calculate end time
                    appointment_datetime = datetime.combine(
                        form.cleaned_data['scheduleDay'],
                        form.cleaned_data['appointmentTime']
                    )
                    appointment_end = appointment_datetime + total_duration
                    
                    appointment.appointmentEndTime = appointment_end.time()
                    appointment.save()
                    form.save_m2m()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Appointment booked successfully!',
                        'appointment_id': appointment.id
                    })
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below',
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def get_available_slots(request):
    """Get available time slots for a specific date and employee"""
    if request.method == 'GET':
        date_str = request.GET.get('date')
        employee_id = request.GET.get('employee_id')
        
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            employee = EmployeeProfile.objects.get(id=employee_id)
            
            # Get existing appointments for this date and employee
            existing_appointments = salonAppointment.objects.filter(
                employeeId=employee,
                scheduleDay=selected_date
            ).order_by('appointmentTime')
            
            # Generate available slots (9 AM to 6 PM, 30-minute intervals)
            available_slots = []
            start_time = datetime.strptime('09:00', '%H:%M').time()
            end_time = datetime.strptime('18:00', '%H:%M').time()
            
            current_time = datetime.combine(selected_date, start_time)
            end_datetime = datetime.combine(selected_date, end_time)
            
            while current_time < end_datetime:
                slot_time = current_time.time()
                
                # Check if this slot is available
                is_available = True
                for appointment in existing_appointments:
                    if (appointment.appointmentTime <= slot_time < appointment.appointmentEndTime):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append(slot_time.strftime('%H:%M'))
                
                current_time += timedelta(minutes=30)
            
            return JsonResponse({
                'success': True,
                'available_slots': available_slots
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def get_service_details(request):
    """Get details for selected services"""
    if request.method == 'GET':
        service_ids = request.GET.get('services', '').split(',')
        
        try:
            services = service.objects.filter(id__in=service_ids)
            
            total_price = sum(service.price for service in services)
            total_duration = timedelta()
            
            for service_obj in services:
                duration_str = service_obj.durationOfService
                duration_parts = duration_str.split()
                
                for i in range(0, len(duration_parts), 2):
                    if i + 1 < len(duration_parts):
                        value = int(duration_parts[i])
                        unit = duration_parts[i + 1]
                        if 'hour' in unit:
                            total_duration += timedelta(hours=value)
                        elif 'minute' in unit:
                            total_duration += timedelta(minutes=value)
            
            total_minutes = total_duration.total_seconds() / 60
            
            return JsonResponse({
                'success': True,
                'total_price': total_price,
                'total_duration': int(total_minutes),
                'services': [{'name': s.service_name, 'price': s.price} for s in services]
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
