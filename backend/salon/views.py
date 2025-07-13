from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from .forms import ServiceForm, AppointmentsForm, ServicesGivenForm
from .models import service

def homepage(request):

    return render(request, '../templates/home.html')

def services_given(request):
    return render(request, 'salon/services_given.html')

class ServicesListView(ListView):
    model = service
    template_name = 'salon/services_list.html'



def appointments(request):
    return render(request, 'salon/appointments.html')


def add_services(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service saved successfully')
            return redirect('services')
            # the redirect should match the view class

    else:
        form = ServiceForm()
        messages.success(request, 'Service has not been saved successfully')
    
    return render(request, 'salon/add_services.html', {'form': form})



def add_appointments(request):
    if request.method == 'POST':
        form = AppointmentsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment saved successfully')
            return redirect('appointments')
            # the redirect should match the view class
    else:
        form = AppointmentsForm()
        messages.success(request, 'Appointment has not been saved successfully')

    
    return render(request, 'salon/add_appointments.html', {'form': form})


def add_services_given(request):
    if request.method == 'POST':
        form = ServicesGivenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service given has been saved successfully')
            return redirect('add-services-given')
            # the redirect should match the view class
        
    else:
        form = ServicesGivenForm()
        messages.success(request, 'Service given has not been saved successfully')

    
    return render(request, 'salon/add_services_given.html', {'form': form})




