from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),

    # path('services/', views.services_report, name='service_report'),

    path('appointments/', views.appointment_report, name='appointments_report'),

    # path('services-given/', views.services_given_report, name='services_given_report'),

    path('employees/', views.employee_report, name='employee_report'),
    
    # path('customers/', views.customers_report, name='customers_report')

]



    