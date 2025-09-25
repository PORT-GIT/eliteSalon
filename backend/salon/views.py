from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, QueryDict
import json
from django import forms
from .forms import ServiceForm, ServicesGivenForm, AppointmentBookingForm
from .models import service, salonAppointment, servicesGiven
from users.models import EmployeeProfile, CustomerProfile
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from formtools.wizard.views import SessionWizardView
from django.db.models import Count, Q
from django.utils import timezone

def services_list(request):
    
    return render(request, 'salon/services_list.html')

@login_required
def services_given_survey(request, appointment_id=None):
    from .forms import ServicesGivenForm
    from django.contrib import messages

    if request.method == 'POST':
        form = ServicesGivenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('services-given-survey')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {}
        if appointment_id:
            try:
                appointment = salonAppointment.objects.get(id=appointment_id)
                initial_data = {
                    'salonAppointmentId': appointment,
                    'customerId': appointment.customerId,
                    'employeeId': appointment.employeeId,
                    # For multiple services, this might need adjustment
                    'servicesId': appointment.services.first() if appointment.services.exists() else None
                }
            except salonAppointment.DoesNotExist:
                messages.error(request, 'Appointment not found.')
                return redirect('services-given-survey')
        form = ServicesGivenForm(initial=initial_data)

    context = {
        'form': form,
        'is_customer': hasattr(request.user, 'customer_profile'),
        'is_employee': hasattr(request.user, 'employee_profile'),
        'is_admin': request.user.is_superuser or request.user.is_staff,
        'appointment_id': appointment_id,
    }
    return render(request, 'salon/services_given_survey.html', context)

def about_us(request):
    return render(request, 'salon/about-us.html')


@login_required
def booking_calendar(request):
    """Display the interactive booking calendar"""
    services = service.objects.all()
    employees = EmployeeProfile.objects.all()
    today = timezone.now().date()

    # this will count and display the history of appointments of the logged in user
    user=request.user
    try:
        customer_profile = user.customer_profile
        appointments = customer_profile.salonappointment_set.all()
        appointments_count = appointments.count()

    except CustomerProfile.DoesNotExist:
        appointments = []
        appointments_count = 0
        

    return render(request, 'salon/booking_calendar.html', {
        'services': services,
        'employees': employees,
        'today': timezone.now().date(),
        'appointments': appointments, #this will assist in calling the appointments to the booking template so that it can
         # be filtered to show as per the person who has logged in
        'appointments_count': appointments_count
    })

    
    

@login_required
@csrf_exempt
def book_appointment_ajax(request):
    """Handle appointment booking via AJAX"""
    if request.method == 'POST':
        # Parse form data from request
        services_str = request.POST.get('services', '')
        data = {
            'services': [sid.strip() for sid in services_str.split(',') if sid.strip()],
            'scheduleDay': request.POST.get('scheduleDay'),
            'appointmentTime': request.POST.get('appointmentTime'),
            'employeeId': request.POST.get('employeeId')
        }

        # Check if user has a customer profile
        if not hasattr(request.user, 'customer_profile'):
            return JsonResponse({
                'success': False,
                'message': 'User does not have a customer profile'
            })

        # Create a QueryDict from the parsed data
        form_data = QueryDict(mutable=True)
        for key, value in data.items():
            if key == 'services' and isinstance(value, list):
                # For multiple choice fields, add each value separately
                for service_id in value:
                    form_data.appendlist(key, service_id)
            else:
                form_data[key] = value

        form = AppointmentBookingForm(form_data, customer=request.user.customer_profile)

        if form.is_valid():
            try:
                with transaction.atomic():
                    appointment = form.save(commit=False)
                    appointment.customerId = request.user.customer_profile

                    # Calculate end time based on services
                    services = form.cleaned_data['services']
                    total_duration = timedelta()

                    for service_obj in services:
                        total_duration += service_obj.new_durationOfService

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
                    'message': f'Error saving appointment: {str(e)}'
                })
    else:
        print("Form errors:", form.errors)
        return JsonResponse({
            'success': False,
            'message': 'Please correct the errors below',
            'errors': form.errors
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def get_available_employees(request):
    """Get available employees for selected services, date, and time"""
    service_ids = request.GET.getlist('services[]')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')

    if not (service_ids and date_str and time_str):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Calculate total duration of selected services
    # total_duration = timedelta()
    # for sid in service_ids:
    #     try:
    #         s = service.objects.get(pk=sid)
    #         total_duration += parse_duration(s.durationOfService)
    #     except service.DoesNotExist:
    #         continue

    try:
        schedule_day = datetime.strptime(date_str, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time_str, '%H:%M').time()
        appointment_start = datetime.combine(schedule_day, appointment_time)
        # appointment_end = appointment_start + total_duration
    except ValueError:
        return JsonResponse({'error': 'Invalid date or time format'}, status=400)

    # Get employees who are free during the requested time slot
    available_employees = []
    for emp in EmployeeProfile.objects.filter(is_active=True):
        # Check if employee has any conflicting appointments
        conflict = salonAppointment.objects.filter(
            employeeId=emp,
            scheduleDay=schedule_day,
            # appointmentTime__lt=appointment_end.time(),
            appointmentEndTime__gt=appointment_time
        ).exists()

        if not conflict:
            available_employees.append({
                'id': emp.id,
                'name': f"{emp.user_profile.first_name} {emp.user_profile.last_name}"
            })

    return JsonResponse({'employees': available_employees})

def get_available_slots(request):
    """Get available time slots for selected employee and services"""
    employee_id = request.GET.get('employee_id')
    service_ids_str = request.GET.get('services', '')
    date_str = request.GET.get('date')

    if not (employee_id and date_str):
        return JsonResponse({'success': False, 'message': 'Missing parameters'}, status=400)

    if service_ids_str:
        service_ids = [sid.strip() for sid in service_ids_str.split(',') if sid.strip()]
    else:
        service_ids = []

    # Calculate total duration of selected services
    total_duration = timedelta()
    for sid in service_ids:
        try:
            s = service.objects.get(pk=sid)
            total_duration += s.new_durationOfService
        except service.DoesNotExist:
            continue

    try:
        schedule_day = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid date format'}, status=400)

    # Consider salon working hours (9 AM to 6 PM)
    start_time = datetime.combine(schedule_day, time(9, 0))
    end_time = datetime.combine(schedule_day, time(18, 0))

    available_slots = []
    current_time = start_time

    while current_time + total_duration <= end_time:
        slot_start = current_time
        slot_end = current_time + total_duration

        # Check for conflicts with existing appointments
        conflict = salonAppointment.objects.filter(
            employeeId_id=employee_id,
            scheduleDay=schedule_day,
            appointmentTime__lt=slot_end.time(),
            appointmentEndTime__gt=slot_start.time()
        ).exists()

        if not conflict:
            available_slots.append(slot_start.strftime('%H:%M'))

        # Move to next slot (15-minute intervals)
        current_time += timedelta(minutes=15)

    return JsonResponse({'success': True, 'available_slots': available_slots})

def get_service_details(request):
    # this will get details for selected services
    if request.method == 'GET':
        service_ids = request.GET.get('services', '').split(',')
        if not service_ids or service_ids[0] == '':
            return JsonResponse({
                'success': True,
                'total_price': 0,
                'total_duration': 0,
                'services': []
            })

        try:
            services = service.objects.filter(id__in=service_ids)

            total_price = sum(s.price for s in services)
            total_duration = timedelta()

            for service_obj in services:
                if service_obj.new_durationOfService:
                    total_duration += service_obj.new_durationOfService

            total_minutes = int(total_duration.total_seconds() // 60)

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


