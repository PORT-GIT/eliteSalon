from django.db import models
from django. contrib.auth.models import AbstractUser

# Create your models here.
class customUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EMPLOYEE', 'Employee'),
        ('CUSTOMER', 'Customer'),
    )
    username = models.CharField(max_length=25, unique=True)
    phoneNumber = models.CharField(max_length=20, null=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER', null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.email
#using this also changes the data fields for creating a superuser so i have gone back to use username instead of email

class adminProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, related_name='admin_profile')
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)

class employeeProfile(models.Model):
    EMPLOYEEWORK_STATUS = (
        ('FREE', 'Free'),
        ('BUSY', 'Busy'),
        ('AT BREAK', 'At break'),
    )

    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, related_name='employee_profile')
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    dateOfBirth = models.DateField(max_length=20)
    skills = models.CharField (max_length=100)
    serviceOffered = models.ManyToManyField('services.services')#this imports the services model from the services
    workStatus = models.CharField(max_length=20, choices=EMPLOYEEWORK_STATUS, default='FREE')
    employmentDate = models.DateField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    #The value set by auto_now will be updated on every call to the .save() method of the model instance.

class customerProfile(models.Model):
    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, related_name='customer_profile')
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    dateOfBirth = models.DateField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True) 
    #The value set by auto_now will be updated on every call to the .save() method of the model instance.
