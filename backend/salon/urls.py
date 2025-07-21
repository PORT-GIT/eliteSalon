from django.urls import path
from . import views


urlpatterns = [
    path('create-services/', views.create_services, name='create-service'),

    path('create-appointments/', views.create_appointments, name='create-appointments'),

    path('create-services-given/', views.create_services_given, name='create-services-given'),

    path('services-given/', views.ServicesGivenListView.as_view(), name='services-given'),

    path('appointments/', views.AppointmentsListView.as_view(), name='appointments'),

    path('services/', views.ServicesListView.as_view(), name='services'),

    path('homepage/', views.homepage, name='homepage'),



]