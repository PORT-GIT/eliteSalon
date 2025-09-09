from django.urls import path
from . import views

urlpatterns = [

    # path('book-appointments/', views.book_appointments, name='book-appointments'),

    path('services-list/', views.services_list, name='services-list'),


    path('about-us/', views.about_us, name='about-us'),

    path('services-given-survey/', views.services_given_survey, name='services-given-survey'),
    path('services-given-survey/<int:appointment_id>/', views.services_given_survey, name='services-given-survey-with-id'),

    # path('services/', views.ServicesListView.as_view(), name='services'),

    # New booking calendar URLs
    path('booking-calendar/', views.booking_calendar, name='booking-calendar'),

    path('book-appointment/', views.book_appointment_ajax, name='book-appointment-ajax'),

    path('get-available-slots/', views.get_available_slots, name='get-available-slots'),

    path('get-service-details/', views.get_service_details, name='get-service-details'),

    path('get-available-employees/', views.get_available_employees, name='get-available-employees'),



]
