from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),

    path('services-report/', views.services_report, name='service_report'),

    path('appointments/', views.appointment_report, name='appointments_report'),

    path('services-given/', views.services_given_report, name='services_given_report'),

    path('employees/', views.employee_report, name='employee_report'),
    
    path('customers/', views.customers_report, name='customers_report')

]



    