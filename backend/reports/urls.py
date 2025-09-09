from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),

    path('employee-list/', views.employee_list, name='employee_list'),
    
    path('customer-list/', views.customer_list, name='customer_list'),

    path('appointment-list/', views.appointment_list, name='appointment_list'),

    # path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),

    # path('appointments/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='delete-appointment'),

    path('services-report/', views.services_report, name='service_report'),

    # path('appointments/', views.appointment_report, name='appointments_report'),

    path('services-given/', views.services_given_report, name='services_given_report'),

    path('employees/', views.employee_report, name='employee_report'),
    
    path('customers/', views.customers_report, name='customers_report'),

    path('valuable-reports/', views.valuable_reports, name='valuable_reports'),

    

]



    