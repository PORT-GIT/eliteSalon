from django.db import models
from users.models import CustomerProfile, EmployeeProfile
# Create your models here.
class service(models.Model):
    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    category = models.CharField(null=False, max_length=25)
    service_name = models.CharField(null=False, max_length=25,unique=True)
    price = models.IntegerField(null=False)
    description = models.TextField(null=False, max_length=400)
    new_durationOfService = models.DurationField(null=True, blank=False)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'services'

    def __str__(self):
        return self.service_name

    @property
    def formatted_duration(self):
        if self.new_durationOfService:
            total_seconds = int(self.new_durationOfService.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            if hours > 0:
                if minutes > 0:
                    return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
                else:
                    return f"{hours} hour{'s' if hours > 1 else ''}"
            else:
                return f"{minutes} minute{'s' if minutes != 1 else ''}"
        return "0 minutes"

class salonAppointment(models.Model):
    APPOINTMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    customerId = models.ForeignKey('users.CustomerProfile', on_delete=models.CASCADE)
    services = models.ManyToManyField(service, related_name="salon_appointment")
    total_price = models.IntegerField(null=True)
    # this will allow me to call on the data stored in this field to be displayed in other templates
    employeeId = models.ForeignKey('users.EmployeeProfile', on_delete=models.CASCADE)
    scheduleDay = models.DateField()
    appointmentTime = models.TimeField(null=False, blank=False)
    appointmentEndTime = models.TimeField(null=False, blank=False)
    # this will allow me to store the calculated time of the appointment and also the time it will end
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    
    def __str__(self):
     return f" {self.customerId} - {self.employeeId} - {self.scheduleDay}"

class servicesGiven(models.Model):
    RATINGS = (
    (1,'1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    )
    # change selection from string
    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    salonAppointmentId = models.ForeignKey(salonAppointment, on_delete=models.SET_NULL, null=True, to_field='id')#sometimes a client cannot have an appointment  
    servicesId = models.ForeignKey(service, to_field='id', on_delete=models.CASCADE)
    customerId = models.ForeignKey(CustomerProfile,  on_delete=models.CASCADE, to_field='id')
    employeeId = models.ForeignKey(EmployeeProfile,  on_delete=models.CASCADE, to_field='id')
    customerRating = models.IntegerField(choices=RATINGS, null=True, blank=True)
    customerComment = models.TextField(null=True, blank=True, max_length=200)
    employeeRating = models.IntegerField(choices=RATINGS, null=True, blank=True)
    employeeComment = models.TextField(null=True, blank=True, max_length=200)

    def __str__(self):
        if self.salonAppointmentId:
            return f"Review for {str(self.salonAppointmentId)}"
        else:
            return f"Review by {str(self.customerId)}"
