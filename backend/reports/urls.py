from django.urls import path
from . import views

urlpatterns = [

    path('', views.reports_home, name='reports_home'),

    path('services/', views.services_report, name='services_report'),

    path('appointments/', views.appointments_report, name='appointments_report'),

    path('services-given/', views.services_given_report, name='services_given_report'),

    path('employees/', views.employees_report, name='employees_report'),
    
    path('customers/', views.customers_report, name='customers_report'),
    ]