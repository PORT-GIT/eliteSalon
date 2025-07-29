from django.shortcuts import render
# from slick_reporting.views import ReportView
from django.db.models import Count, Sum, Avg
from salon.models import service, salonAppointment, servicesGiven
from users.models import CustomerProfile, EmployeeProfile
# this are for the reports UI
import json


def reports_dashboard(request):
    return render(request, 'reports/dashboard.html')

def appointment_report(request):
    appointments = salonAppointment.objects.all()
    
    # Add simple filters
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(appointmentStatus=status)
    
    return render(request, 'reports/appointment_reports.html', {
        'appointments': appointments
    })

def services_report(request):
    services_data = service.objects.annotate(
        total_given=Count('servicesgiven')
    ).values('service_name', 'total_given')

    service_names = [item['service_name'] for item in services_data]
    service_counts = [item['total_given'] for item in services_data]

    context = {
        'service_names': json.dumps(service_names),
        'service_counts': json.dumps(service_counts),
        'total_services': service.objects.count(),
    }
    return render(request, 'reports/services_reports.html', context)

# def services_report(request):
#     services_data = servicesGiven.objects.values(
#         'servicesGiven__service_name'
#     ).annotate(
#         total=Count('id'),
#         avg_rating=Avg('customerRating')
#     )
#     return render(request, 'reports/services_reports.html', {
#         'service': services_data
#     })

def employee_report(request):
    employees = EmployeeProfile.objects.annotate(
        appointments_count=Count('salonappointment'),
        avg_rating=Avg('servicesgiven__employeeRating')
    )
    return render(request, 'reports/employees_reports.html', {
        'employees': employees
    })

def services_given_report(request):
    pass

def customers_report(request):
    pass

