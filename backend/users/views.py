from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from .forms import EmployeeRegistrationForm, CustomerRegistrationForm
from .models import EmployeeProfile, CustomerProfile
from salon.models import salonAppointment
from django.contrib.auth.decorators import login_required

# this is a view for the homepage 
def homepage(request):
    return render(request, 'users/home.html')

@login_required
def logged_customer(request):
    # this will count and display the history of appointments of the logged in user
    user=request.user
    try:
        customer_profile = user.customer_profile
        appointments = customer_profile.salonappointment_set.all()
        appointments_count = appointments.count()

    except CustomerProfile.DoesNotExist:
        appointments = []
        appointments_count = 0
    return render(request, 'users/logged-customer.html', {
        'appointments': appointments, #this will assist in calling the appointments to the booking template so that it can
         # be filtered to show as per the person who has logged in
        'appointments_count': appointments_count
    })

@login_required
def employee_profile(request):
    user = request.user
    try:
        employee_profile = user.employee_profile
        appointments = employee_profile.salonappointment_set.all()
        appointments_count = appointments.count()  
        # Count appointments for the employee who has logged in

    except EmployeeProfile.DoesNotExist:
        appointments = []
        appointments_count = 0

    return render(request, 'users/employee-profile.html', {
        'appointments': appointments,
        'appointments_count': appointments_count
    })

def admin_dashboard(request):
    employee_count = EmployeeProfile.objects.count()
    customer_count = CustomerProfile.objects.count()
    appointments_count = salonAppointment.objects.count()

    # this will query the database and find out how many customers have more than one appointments
    repeat_customers = CustomerProfile.objects.annotate(
        appointments_count=Count('salonappointment')
    ).filter(appointments_count__gt=1)
    return render(request, 'users/dashboard.html',{
        'employee_count':employee_count, 
        'customer_count':customer_count,
        'appointments_count': appointments_count,
        'repeat_customers': repeat_customers,
    })

# @admin_required
def delete_employee(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == 'POST':
        employee.user_profile.delete()
        return redirect('employee_list') 
        #this will redirect to the employee list after deletion
    return redirect('reports/dashboard.html')

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
                if user.is_superuser:
                    return redirect('admin_dashboard')
                elif hasattr(user, 'employee_profile'):
                    return redirect('employee-profile')
                else:
                    return redirect('booking-calendar')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    # for any conditional statement about log-outs
    # i need to confirm the stype of user before logging out so that they are directed to the required place
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logout(request)
            return redirect('login')
          
        else:
            logout(request)
            return redirect('homepage')

    #if user is not authenticated they go to homepage

    return redirect('homepage')




