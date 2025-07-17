from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, customerProfile, employeeProfile
from salon.models import service
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active', 'groups', 'user_permissions']
        
# i have specified the fields otherwise all fields will be rendered

class CustomerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'date_of_birth']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists!") 
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = CustomUser.CUSTOMER
        #this sets the role automatically
        if commit:
            user.save()

        return user
    

class CustomerProfileForm(forms.ModelForm):
    services_to_offer = forms.ModelMultipleChoiceField(queryset=service.objects.all(),
     widget=forms.CheckboxSelectMultiple, required=True)
    class Meta:
        model = customerProfile
        fields = ['phone_number', 'date_of_birth']


class EmployeeRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists!") 
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = CustomUser.EMPLOYEE
        #this sets the role automatically
        if commit:
            user.save()

        return user
        

class EmployeeProfileForm(forms.ModelForm):
    services_to_offer = forms.ModelMultipleChoiceField(queryset=service.objects.all(),
     widget=forms.CheckboxSelectMultiple, required=True)
    class Meta:
        model = employeeProfile
        fields = ['phone_number', 'date_of_birth', 'services_to_offer']
        