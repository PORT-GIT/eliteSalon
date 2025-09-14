from django.shortcuts import render
# from slick_reporting.views import ReportView
from django.db.models import Count, Sum, Avg
from salon.models import service, salonAppointment, servicesGiven
from users.models import CustomerProfile, EmployeeProfile
# this are for the reports UI
import json

def dashboard(request):
    return render(request, 'reports/dashboard.html')

def customer_list(request):
    customers = CustomerProfile.objects.all().select_related('user_profile')
    return render(request, 'reports/list_of_customers.html', {'customers': customers})

def employee_list(request):
    employees = EmployeeProfile.objects.all().select_related('user_profile')
    return render(request, 'reports/list_of_employees.html', {'employees': employees})

def appointment_list(request):
    appointments = salonAppointment.objects.all().select_related('customerId__user_profile', 'employeeId__user_profile')

    # this add filters
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(appointmentStatus=status)
        
    return render(request, 'reports/list_of_appointments.html', {'appointments': appointments})

# def appointment_report(request):
#     appointments = salonAppointment.objects.all()
    
#     # Add simple filters
#     status = request.GET.get('status')
#     if status:
#         appointments = appointments.filter(appointmentStatus=status)
    
#     return render(request, 'reports/appointment_reports.html', {
#         'appointments': appointments
#     })

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

def valuable_reports(request):
    import csv
    from django.http import HttpResponse
    from io import StringIO
    from django.db.models.functions import TruncDate

    # Appointments over time
    appointments_over_time = salonAppointment.objects.annotate(day=TruncDate('scheduleDay')).values('day').annotate(count=Count('id')).order_by('day')
    days = [str(item['day']) for item in appointments_over_time]
    appointment_counts = [item['count'] for item in appointments_over_time]

    # Popular services
    popular_services = service.objects.annotate(count=Count('salon_appointment')).order_by('-count')[:10]
    service_names = [s.service_name for s in popular_services]
    service_popularity = [s.count for s in popular_services]

    # Service prices
    service_prices = service.objects.values('service_name', 'price')
    price_names = [s['service_name'] for s in service_prices]
    prices = [s['price'] for s in service_prices]

    # Employee performance
    employee_performance = EmployeeProfile.objects.annotate(appointment_count=Count('salonappointment')).order_by('-appointment_count')
    employee_names = [e.user_profile.get_full_name() for e in employee_performance]
    employee_appointments = [e.appointment_count for e in employee_performance]

    download_format = request.GET.get('download')

    if download_format == 'csv':
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="valuable_reports.csv"'

        writer = csv.writer(response)
        writer.writerow(['Appointments Over Time'])
        writer.writerow(['Date', 'Count'])
        for day, count in zip(days, appointment_counts):
            writer.writerow([day, count])

        writer.writerow([])
        writer.writerow(['Popular Services'])
        writer.writerow(['Service Name', 'Count'])
        for name, count in zip(service_names, service_popularity):
            writer.writerow([name, count])

        writer.writerow([])
        writer.writerow(['Service Prices'])
        writer.writerow(['Service Name', 'Price'])
        for name, price in zip(price_names, prices):
            writer.writerow([name, price])

        writer.writerow([])
        writer.writerow(['Employee Performance'])
        writer.writerow(['Employee Name', 'Appointment Count'])
        for name, count in zip(employee_names, employee_appointments):
            writer.writerow([name, count])

        return response

    elif download_format == 'pdf':
        # Create PDF response
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesizes=letter)

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Valuable Reports and Insights")

        y = 720
        p.setFont("Helvetica", 12)

        # Appointments Over Time
        p.drawString(100, y, "Appointments Over Time")
        y -= 20
        for day, count in zip(days, appointment_counts):
            p.drawString(100, y, f"{day}: {count}")
            y -= 15
            if y < 50:
                p.showPage()
                y = 750

        # Popular Services
        p.drawString(100, y, "Popular Services")
        y -= 20
        for name, count in zip(service_names, service_popularity):
            p.drawString(100, y, f"{name}: {count}")
            y -= 15
            if y < 50:
                p.showPage()
                y = 750

        # Service Prices
        p.drawString(100, y, "Service Prices")
        y -= 20
        for name, price in zip(price_names, prices):
            p.drawString(100, y, f"{name}: ${price}")
            y -= 15
            if y < 50:
                p.showPage()
                y = 750

        # Employee Performance
        p.drawString(100, y, "Employee Performance")
        y -= 20
        for name, count in zip(employee_names, employee_appointments):
            p.drawString(100, y, f"{name}: {count} appointments")
            y -= 15
            if y < 50:
                p.showPage()
                y = 750

        p.showPage()
        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="valuable_reports.pdf"'
        return response

    context = {
        'days': json.dumps(days),
        'appointment_counts': json.dumps(appointment_counts),
        'service_names': json.dumps(service_names),
        'service_popularity': json.dumps(service_popularity),
        'price_names': json.dumps(price_names),
        'prices': json.dumps(prices),
        'employee_names': json.dumps(employee_names),
        'employee_appointments': json.dumps(employee_appointments),
    }
    return render(request, 'reports/valuable_reports.html', context)

