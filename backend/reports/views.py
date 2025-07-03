# from django.shortcuts import render
# from django.db.models import Count, Sum, Avg
# from services.models import salonAppointment, servicesGiven, services
# from users.models import employeeProfile, customerProfile

# #dashboard for reports
# def reports_dashboard(request):
#     return render(request, 'reports/dashboard.html')

# # the services reports
# def services_report(request):
#     services = services.objects.all()
#     return render(request, 'reports/services_reports.html', {'services': services})

# # the appointments reports
# def appointments_report(request):
#     appointments = salonAppointment.objects.select_related(
#         'customerId', 'employeeId', 'serviceId'
#     ).all()
#     return render(request, 'reports/appointment_reports.html', {'appointments': appointments})

# # the employee performance reports
# def employee_performance(request):
#     employees = employeeProfile.objects.annotate(
#         total_appointments=Count('salonappointment')
#     ).prefetch_related('serviceOffered')
#     return render(request, 'reports/employees_reports.html', {'employees': employees})

# #revenue by service
# def revenue_report(request):
#     revenue_data = servicesGiven.objects.values(
#         'servicesGiven__serviceName'
#     ).annotate(
#         total_revenue=Sum('servicesGiven__price')
#     )
#     return render(request, 'reports/revenue_reports.html', {'revenue_data': revenue_data})

# #customer activity
# def customer_activity(request):
#     customers = customerProfile.objects.annotate(
#         appointment_count=Count('salonappointment')
#     ).order_by('-appointment_count')
#     return render(request, 'reports/customer_reports.html', {'customers': customers})

# #popular services
# def service_utilization(request):
#     popular_services = services.objects.annotate(
#         use_count=Count('servicesgiven')
#     ).order_by('-use_count')
#     return render(request, 'reports/services_given_reports.html', {'services': popular_services})


