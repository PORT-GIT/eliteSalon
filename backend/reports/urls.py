from django.urls import path
from . import views

urlpatterns = [
    

    path('employee-list/', views.employee_list, name='employee-list'),
    
    path('customer-list/', views.customer_list, name='customer-list'),

    path('appointment-list/', views.appointment_list, name='appointment_list'),

    path('surveys-list/', views.surveys_list, name="surveys-list"),

    path('services-report/', views.services_report, name='service_report'),

    # path('appointments/', views.appointment_report, name='appointments_report'),

    path('services-given/', views.services_given_report, name='services_given_report'),

    path('employees/', views.employee_report, name='employee_report'),
    
    path('customers/', views.customers_report, name='customers_report'),

    path('valuable-reports/', views.valuable_reports, name='valuable_reports'),

    

]



    