from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.chat, name="chat"),

    path('register/employee', views.EmployeeRegistration.as_view(), name='employee-registration'),

    path('register/employee', views.CustomerRegistration.as_view(), name='customer-registration'),
]

