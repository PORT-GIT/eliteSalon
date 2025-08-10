from django.urls import path
from . import views
from .appointment_form_wizard import SelectServicesForm, SelectDateForm, ConfirmDetailsForm, EmployeeSelectionForm
from .views import AppointmentWizard


FORMS = [
    ("select_services", SelectServicesForm),
    ("select_date", SelectDateForm),
    ("select_employee", EmployeeSelectionForm),
    ("confirm", ConfirmDetailsForm),
]

TEMPLATES = [
    ("select_services", "salon/select_services.html"),
    ("select_date", "salon/select_date.html"),
    ("select_employee", "salon/select_employee.html"),
    ("confirm" , "salon/confirm_details.html"),
]


urlpatterns = [
    path('create-services/', views.create_services, name='create-service'),

    # path('create-appointments/', AppointmentWizard.as_view(), name='create-appointments'),

    path('book-appointments/', views.book_appointments, name='book-appointments'),

    path('create-services-given/', views.create_services_given, name='create-services-given'),

    path('services-list/', views.list_of_services, name='services-list'),

    path('about-us/', views.about_us, name='about-us'),

    path('services-given/', views.ServicesGivenListView.as_view(), name='services-given'),

    path('appointments/', views.AppointmentsListView.as_view(), name='appointments'),

    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),

    path('appointments/<int:pk>/delete', views.AppointmentDeleteView.as_view(), name='delete-appointment'),

    # path('services/', views.ServicesListView.as_view(), name='services'),

]