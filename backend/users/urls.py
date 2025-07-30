from django.urls import path
from . import views

urlpatterns = [
    
    # path("", views.chat, name="chat"),

    path('register-employee/', views.register_employee, name='register-employee'),

    path('register-customer/', views.register_customer, name='register-customer'),

    path('login/', views.user_login, name='login'),

    # path('logout/', views.user_logout, name='user-logout'),

    path('', views.homepage, name='homepage'),
    # this will ensure that the homepage is accessible at the root URL

    path('contact-us/', views.contact_us, name='contact-us'),
    
]


