from django.shortcuts import render
from services.models import salonAppointment, servicesGiven, services
from users.models import employeeProfile, customerProfile

# Create your views here.
# Services Report
def services_report(request):
    services = services.objects.all()
    return render(request, 'reports/services.html', {'services': services})

# Appointments Report
def appointments_report(request):
    appointments = salonAppointment.objects.select_related(
        'customerId', 'employeeId', 'serviceId'
    ).all()
    return render(request, 'reports/appointments.html', {'appointments': appointments})

# Employee Performance Report
def employee_performance(request):
    employees = employeeProfile.objects.annotate(
        total_appointments=Count('salonappointment')
    ).prefetch_related('serviceOffered')
    return render(request, 'reports/employees.html', {'employees': employees})

#revenue by service
def revenue_report(request):
    revenue_data = servicesGiven.objects.values(
        'servicesGiven__serviceName'
    ).annotate(
        total_revenue=Sum('servicesGiven__price')
    )
    return render(request, 'reports/revenue.html', {'revenue_data': revenue_data})

#customer activity
def customer_activity(request):
    customers = customerProfile.objects.annotate(
        appointment_count=Count('salonappointment')
    ).order_by('-appointment_count')
    return render(request, 'reports/customers.html', {'customers': customers})

#popular services
def service_utilization(request):
    popular_services = services.objects.annotate(
        use_count=Count('servicesgiven')
    ).order_by('-use_count')
    return render(request, 'reports/service_usage.html', {'services': popular_services})