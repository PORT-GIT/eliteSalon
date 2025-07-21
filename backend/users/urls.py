from django.urls import path
from . import views

urlpatterns = [
    
    # path("", views.chat, name="chat"),

    path('register-employee/', views.register_employee, name='register-employee'),

    path('register-customer/', views.register_customer, name='register-customer'),

    # path('login/', views.user_login, name='user-login'),

    # path('logout/', views.user_logout, name='user-logout'),

    
]


