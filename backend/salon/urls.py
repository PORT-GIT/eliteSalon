from django.urls import path
from . import views

urlpatterns = [
    path('create-services/', views.create_services, name='create-service'),

    # path('book-appointments/', views.book_appointments, name='book-appointments'),

    path('create-services-given/', views.create_services_given, name='create-services-given'),

    path('services-list/', views.list_of_services, name='services-list'),

    path('about-us/', views.about_us, name='about-us'),

    path('services-given/', views.ServicesGivenListView.as_view(), name='services-given'),

    path('appointments/', views.AppointmentsListView.as_view(), name='appointments'),

    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),

    path('appointments/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='delete-appointment'),

    # path('services/', views.ServicesListView.as_view(), name='services'),

    # New booking calendar URLs
    path('booking-calendar/', views.booking_calendar, name='booking-calendar'),

    path('book-appointment/', views.book_appointment_ajax, name='book-appointment-ajax'),

    path('get-available-slots/', views.get_available_slots, name='get-available-slots'),

    path('get-service-details/', views.get_service_details, name='get-service-details'),

    path('get-available-employees/', views.get_available_employees, name='get-available-employees'),



]
