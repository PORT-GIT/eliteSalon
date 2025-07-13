from django.urls import path
from . import views


urlpatterns = [
    path('add-services/', views.add_services, name='add-service'),

    path('add-appointments/', views.add_appointments, name='add-appointments'),

    path('add-services-given/', views.add_services_given, name='add-services-given'),

    path('services-given/', views.services_given, name='services-given'),

    path('appointments/', views.appointments, name='appointments'),

    path('services/', views.ServicesListView.as_view(), name='services'),



]