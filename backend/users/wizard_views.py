from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from .step_forms import EmployeeStep1Form, EmployeeStep2Form, EmployeeStep3Form
from .models import EmployeeProfile
from salon.models import service

class EmployeeRegistrationWizard(View):
    """Multi-step employee registration wizard"""
    
    def get(self, request, step=None):
        """Handle GET requests for each step"""
        if step is None:
            step = 1
            
        if step == 1:
            form = EmployeeStep1Form()
            return render(request, 'users/employee-basic-info1.html', {
                'form': form,
                'step': 1,
                'total_steps': 3
            })
        elif step == 2:
            form = EmployeeStep2Form()
            return render(request, 'users/employee-services2.html', {
                'form': form,
                'step': 2,
                'total_steps': 3
            })
        elif step == 3:
            form = EmployeeStep3Form()
            services = service.objects.all()
            categories = services.values_list('category', flat=True).distinct()
            services_by_category = {
                category: services.filter(category=category)
                for category in categories
            }
            return render(request, 'users/employee-last-step-new.html', {
                'form': form,
                'step': 3,
                'total_steps': 3,
                'categories': categories,
                'services_by_category': services_by_category
            })
        
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = service.objects.all()
        categories = services.values_list('category', flat=True).distinct()
        context['categories'] = [(cat, cat) for cat in categories]
        context['services_by_category'] = {
            category: services.filter(category=category)
            for category in categories
        }
        return context 

    
    def post(self, request, step=None):
        """Handle POST requests for each step"""
        if step is None:
            step = 1
            
        if step == 1:
            form = EmployeeStep1Form(request.POST)
            if form.is_valid():
                # Store step 1 data in session
                request.session['step1_data'] = form.cleaned_data
                return redirect('employee-register-step', step=2)
            return render(request, 'users/employee-basic-info1.html', {
                'form': form,
                'step': 1,
                'total_steps': 3
            })
            
        elif step == 2:
            form = EmployeeStep2Form(request.POST)
            if form.is_valid():
                # Store step 2 data in session
                request.session['step2_data'] = form.cleaned_data
                return redirect('employee-register-step', step=3)
            return render(request, 'users/employee-services2.html', {
                'form': form,
                'step': 2,
                'total_steps': 3
            })
            
        elif step == 3:
            form = EmployeeStep3Form(request.POST)
            if form.is_valid():
                # Get all stored data
                step1_data = request.session.get('step1_data')
                step2_data = request.session.get('step2_data')
                
                if step1_data and step2_data:
                    # this will create user
                    user = User.objects.create_user(
                        username=step1_data['username'],
                        email=step1_data['email'],
                        password=step1_data['password1'],
                        first_name=step1_data['first_name'],
                        last_name=step1_data['last_name']
                    )
                    
                    # this will create employee profile
                    profile = EmployeeProfile.objects.create(
                        user_profile=user,
                        phone_number=step2_data['phone_number'],
                        date_of_birth=step2_data['date_of_birth']
                    )
                    profile.services_to_offer.set(form.cleaned_data['services_to_offer'])
                    
                    # Clean up session data
                    del request.session['step1_data']
                    del request.session['step2_data']
                    
                    # Log the user in
                    login(request, user)
                    messages.success(request, 'Employee registration completed successfully!')
                    return redirect('login')
                else:
                    messages.error(request, 'Registration data is incomplete. Please start over.')
                    return redirect('employee-register-step', step=1)
                    
            return render(request, 'users/employee-last-step-new.html', {
                'form': form,
                'step': 3,
                'total_steps': 3,
                'categories': service.objects.values_list('category', flat=True).distinct(),
                'services_by_category': {category: service.objects.filter(category=category) for category in service.objects.values_list('category', flat=True).distinct()}
            })
