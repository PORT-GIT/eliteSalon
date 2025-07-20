from django.shortcuts import render, redirect
# from .models import CustomerProfile, EmployeeProfile
from .forms import EmployeeRegistrationForm, CustomerRegistrationForm, LoginForm

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('login')
            #this will return the user to the login page

    else:
        form = EmployeeRegistrationForm()
            
        return render(request, 'users/register-employee.html', {'form' : form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('login')
            #this will return the user to the login page
    
    else:
        form = CustomerRegistrationForm()

    return render(request, 'users/register-customer.html', {'form' : form})

def user_login(request):
    if request.method == 'GET':
        form = LoginForm(request.GET)
        if form.is_valid():
            form.save()
            return redirect ('login')
        
    else:
        form = LoginForm()
    return render(request, 'salon/add_appointments.html', {'form' : form})