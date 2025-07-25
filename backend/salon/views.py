from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import ServiceForm, AppointmentsForm, ServicesGivenForm
from .models import service, salonAppointment, servicesGiven
from django.contrib.auth.decorators import login_required


class ServicesGivenListView(ListView):
    model = servicesGiven
    template_name = 'salon/services_given.html'
    context_object_name = 'services-given'

    def get_queryset(self):
        return servicesGiven.objects.all()
    

class ServicesListView(ListView):
    model = service
    template_name = 'salon/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return service.objects.all()


class AppointmentsListView(ListView):
    model = salonAppointment
    template_name = 'salon/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return salonAppointment.objects.all()
    
class AppointmentDetailView(DetailView):
    model = salonAppointment
    template_name = 'salon/appointment_detail.html'

def create_services(request):
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


#to consider the fact that a user won't need to enter their own details i can add the decorator below which will capture their details:
@login_required
def create_appointments(request):
    if request.method == 'POST':
        form = AppointmentsForm(request.POST)
        if form.is_valid():
            # the changes made here and to the form will ensure that the user does not
            # select their details manually
            # instead, the user will be captured automatically
            # it also assigns the logged in user's profile to the appointment model customerID field
            appointment = form.save(commit=False)
            appointment.customerId = request.user.customer_profile
            # customer_profile is added because the user is linked to the customer profile and not the 
            # DJANGO USER model
            appointment.save()
            messages.success(request, 'Appointment saved successfully')
            return redirect('appointments')
            # the redirect should match the view class
    else:
        form = AppointmentsForm()
        messages.success(request, 'Appointment has not been saved successfully')

    
    return render(request, 'salon/add_appointments.html', {'form': form})


def create_services_given(request):
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




