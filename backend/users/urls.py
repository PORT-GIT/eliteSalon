from django.urls import path
from . import views
from .wizard_views import EmployeeRegistrationWizard

urlpatterns = [
    
    # Traditional registration (can be removed if wizard is preferred)
    # path('register-employee/', views.register_employee, name='register-employee'),

    # Multi-step wizard registration
    path('register-employee-wizard/', EmployeeRegistrationWizard.as_view(), name='employee-register-wizard'),
    path('register-employee-wizard/<int:step>/', EmployeeRegistrationWizard.as_view(), name='employee-register-step'),

    path('register-customer/', views.register_customer, name='register-customer'),

    path('login/', views.user_login, name='login'),

    path('delete-employee/<int:pk>/', views.delete_employee, name='delete_employee'),

    path('user-logout/', views.user_logout, name='user-logout'),

    path('', views.homepage, name='homepage'),
    # this will ensure that the homepage is accessible at the root URL

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # this is the URL to the admin dashboard

    # path('redirect-after-login/', views.redirect_after_login, name='redirect-after-login' )

    
]


