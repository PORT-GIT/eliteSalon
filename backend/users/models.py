from django.db import models
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    phone_number = models.CharField(null=False, max_length=25)
    
    # def __str__(self):
    #     return self.username 

class EmployeeProfile(models.Model):

    WORK_STATUS = (
        ('FREE', 'Free'),
        ('BUSY', 'Busy'),
        ('BREAK', 'At break')
    )

    id = models.AutoField(primary_key=True)
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone_number = models.CharField(null=False, max_length=25)
    date_of_birth = models.DateField(null=False, blank=False)
    services_to_offer = models.ManyToManyField('salon.service', verbose_name=('services to offer'), related_name="employee_profile")
    work_status = models.CharField(choices=WORK_STATUS, max_length=20, default='FREE')
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.id)+"    "+ self.user.first_name+"    "+self.user.last_name
    # # this means that the names of the employee will be shown in the UI and admin


class CustomerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(null=False, max_length=25)
    date_of_birth = models.DateField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.user.first_name +"    "+ self.user.last_name
