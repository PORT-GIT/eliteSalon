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

class EmployeeRegistrationForm(BaseProfileForm):
    services_to_offer = forms.ModelMultipleChoiceField(queryset=service.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=True, label='Services to Offer')
    
    class Meta:
        model = User
        fields = ['username'] + COMMON_FIELDS + ['password1', 'password2', 'services_to_offer']

        def save(self, commit = True):
            user = super().save(commit=False)
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

class CustomerRegistrationForm(BaseProfileForm):
    class Meta:
        model = User
        fields = ['username'] + COMMON_FIELDS + ['password1', 'password2']

        def save(self, commit = True):
            user = super().save(commit=False)
            user.save()
            profile = CustomerProfile.objects.create(
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

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type' : 'text'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type' : 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get("password1") != cleaned_data.get("password2"):
                raise forms.ValidationError("Passwords do not match!")
            return cleaned_data

    
    

    
# def clean_email(self):
#     email = self.cleaned_data.get('email')
#     if CustomUser.objects.filter(email=email).exists():
#         raise forms.ValidationError("This email already exists!")
#     return email

# def clean(self):
#     cleaned_data = super().clean()
#     if cleaned_data.get("password1") != cleaned_data.get("password2"):
#         raise forms.ValidationError("Passwords do not match!")
#     return cleaned_data

# def save(self, commit = True):
#     user = super().save(commit=False)
#     user.set_password(self.cleaned_data["password1"])
#     user.role = CustomUser.CUSTOMER
#     # this sets the role automatically
#     if commit:
#         user.save()

#     return user