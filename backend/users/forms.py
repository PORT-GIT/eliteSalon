from django import forms
from .models import EmployeeProfile, CustomerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from salon.models import service

# these are the common fields for the employee and customer profiles
COMMON_FIELDS = [
    'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth'
]

class BaseProfileForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, 
        widget=forms.DateInput(attrs={'type' : 'date'}))
    
    def save(self, commit = True):
        user = super().save(commit=False)#this saves the user if commit =True
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        
        return user

class EmployeeRegistrationForm(BaseProfileForm):
    services_to_offer = forms.ModelMultipleChoiceField(queryset=service.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=True, label='Services to Offer')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this will now add bootstrap classes to the field widgets
        for field_name, field in self.fields.items():
            # i will not need form-control for the multiple selection services fields
            if field_name == 'services_to_offer':
                
                continue
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

            # this will add the placeholder to the field widgets
            field.widget.attrs['placeholder'] = field.label
    
    class Meta:
        model = User
        fields = ['username'] + COMMON_FIELDS + ['password1', 'password2', 'services_to_offer']

    def save(self, commit = True):
        user = super().save(commit=False)#this saves the user if commit =True
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = False
        user.is_superuser = False
        # this makes the customer not have access to the admin panel
        if commit:
            user.save()
        profile = EmployeeProfile.objects.create(
            user_profile=user,
            phone_number=self.cleaned_data['phone_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        ) 
        profile.services_to_offer.set(self.cleaned_data['services_to_offer'])
        return user
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # because the email is a field in the USER model that is why I am relating it to the FK in the employeeprofile
        if EmployeeProfile.objects.filter(user_profile__email=email).exists():
            raise forms.ValidationError("This email already exists!")
        return email
        
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

# class AdminRegistrationForm(BaseProfileForm):
    
#     class Meta:
#         model = User
#         fields = ['username'] + COMMON_FIELDS + ['password1', 'password2', 'services_to_offer']

#     def save(self, commit = True):
#         user = super().save(commit=False)#this saves the user if commit =True
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.is_staff = False
#         user.is_superuser = False
#         # this makes the customer not have access to the admin panel
#         if commit:
#             user.save()
#         profile = EmployeeProfile.objects.create(
#             user_profile=user,
#             phone_number=self.cleaned_data['phone_number'],
#             date_of_birth=self.cleaned_data['date_of_birth'],
#         ) 
#         profile.services_to_offer.set(self.cleaned_data['services_to_offer'])
#         return user
        
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         # because the email is a field in the USER model that is why I am relating it to the FK in the employeeprofile
#         if EmployeeProfile.objects.filter(user_profile__email=email).exists():
#             raise forms.ValidationError("This email already exists!")
#         return email
        
#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get("password1") != cleaned_data.get("password2"):
#             raise forms.ValidationError("Passwords do not match!")
#         return cleaned_data



class CustomerRegistrationForm(BaseProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this will now add bootstrap classes to the field widgets
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

            # this will add the placeholder to the field widgets
            field.widget.attrs['placeholder'] = field.label


    class Meta:
        model = User
        fields = ['username'] + COMMON_FIELDS + ['password1', 'password2']

    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = False
        user.is_superuser = False
        # this makes the customer not have access to the admin panel

        if commit:
            user.save()

        CustomerProfile.objects.create(
            user_profile=user,
            phone_number=self.cleaned_data['phone_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )
        return user
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # because the email is a field in the USER model that is why I am relating it to the FK in the customerprofile   
        if CustomerProfile.objects.filter(user_profile__email=email).exists():
            raise forms.ValidationError("This email already exists!")
        return email
        
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data



class ContactUsForm(forms.ModelForm):
    pass
    
    

    