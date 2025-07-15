from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, customerProfile, employeeProfile
from salon.models import service
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active', 'groups', 'user_permissions']
        
# i have specified the fields otherwise all fields will be rendered

# class CustomerRegistrationForm(UserCreationForm):
#     class Meta:
#         model = customerProfile
#         fields = ['phone_number', 'date_of_birth']

class EmployeeRegistrationForm(UserCreationForm):
    services_to_offer = forms.ModelMultipleChoiceField(queryset=service.objects.all(),
     widget=forms.CheckboxSelectMultiple, required=True, label = 'Services to offer')
    class Meta:
        model = employeeProfile
        fields = ['phone_number', 'date_of_birth', 'services_to_offer',]
        