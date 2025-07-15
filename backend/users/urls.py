from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.chat, name="chat"),

    path('register/employee', views.EmployeeRegistration, name='employee-registration'),
]

