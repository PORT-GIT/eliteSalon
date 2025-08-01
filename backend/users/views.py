from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import EmployeeRegistrationForm, CustomerRegistrationForm
from .decorator import employee_required, customer_required, admin_required

# this is a view for the homepage 
def homepage(request):
    return render(request, 'users/home.html')

def contact_us(request):
    return render(request, 'users/contact-us.html')


@employee_required
def employee_dashboard(request):
    return render(request, 'users/employee_dashboard.html')

@customer_required
def customer_dashboard(request):
    return render(request, 'users/customer_dashboard.html')

@admin_required
def admin_dashboard(request):
    return render(request, 'reports/dashboard.html')

# @employee_required
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            #this will return the user to the login page
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'users/register-employee.html', {'form': form})


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            #this will return the user to the login page
    else:
        form = CustomerRegistrationForm()
    return render(request, 'users/register-customer.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('homepage')

