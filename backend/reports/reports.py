# from django.shortcuts import render
# from django.db.models import Count, Sum, Avg
# from salon.models import service, salonAppointment, servicesGiven
# from users.models import customerProfile, employeeProfile

# def reports_dashboard(request):
#     return render(request, 'reports/dashboard.html')

# def appointment_report(request):
#     appointments = salonAppointment.objects.all()
    
#     # Add simple filters
#     status = request.GET.get('status')
#     if status:
#         appointments = appointments.filter(appointmentStatus=status)
    
#     return render(request, 'reports/appointments.html', {
#         'appointments': appointments
#     })

# def service_report(request):
#     services_data = servicesGiven.objects.values(
#         'servicesGiven__serviceName'
#     ).annotate(
#         total=Count('id'),
#         avg_rating=Avg('customerRating')
#     )
#     return render(request, 'reports/services.html', {
#         'services': services_data
#     })

# def employee_report(request):
#     employees = employeeProfile.objects.annotate(
#         appointments_count=Count('salonappointment'),
#         avg_rating=Avg('servicesgiven__employeeRating')
#     )
#     return render(request, 'reports/employees.html', {
#         'employees': employees
#     })

# from slick_reporting.views import ReportView
# from slick_reporting.fields import SlickReportField
# from salon.models import service
# from django.db.models import Count, Sum