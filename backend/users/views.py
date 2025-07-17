from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import EmployeeRegistrationForm, EmployeeProfileForm, CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db import transaction
# from django.urls import reverse_lazy

# Create your views here.
def chat(request):
    
    return render(request, "base.html")

class EmployeeRegistration(View):
    def get(self, request):
        user_form = EmployeeRegistrationForm()
        profile_form = EmployeeProfileForm()
        return render (request, 'users/register-employee.html', {
            'user_form' : user_form,
            'profile_form' : profile_form
        })
    

    def post(self, request):
        user_form = EmployeeRegistrationForm(request.POST)
        profile_form = EmployeeProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                #these atomic transactions prevent partial saves
                with transaction.atomic():
                    user = user_form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    profile_form.save_m2m()
                    #this saves the many-to_many field for the services

                    messages.success(request, 'Employee was registered successfully')
                    return redirect('login')
            
            except Exception as e :
                messages.error(request, f'Registration failed: {str(e)}')

        for field, errors in profile_form.errors.items():
            for error in errors:
                messages.error(request, f"Profile {field}: {error}") 

        return render (request, 'users/register-employee.html', {
                'user_form' : user_form,
                'profile_form' : profile_form
            })


class CustomerRegistration(View):
    def get(self, request):
        user_form = CustomerRegistrationForm()
        profile_form = CustomerProfileForm()
        return render (request, 'users/register-customer.html', {
            'user_form' : user_form,
            'profile_form' : profile_form
        })
    

    def post(self, request):
        user_form = CustomerRegistrationForm(request.POST)
        profile_form = EmployeeProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                #these atomic transactions prevent partial saves
                with transaction.atomic():
                    user = user_form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    profile_form.save_m2m()
                    #this saves the many-to_many field for the services

                    messages.success(request, 'Employee was registered successfully')
                    return redirect('login')
            
            except Exception as e :
                messages.error(request, f'Registration failed: {str(e)}')

        for field, errors in profile_form.errors.items():
            for error in errors:
                messages.error(request, f"Profile {field}: {error}") 
                   
        return render (request, 'users/register-employee.html', {
                'user_form' : user_form,
                'profile_form' : profile_form
            })
