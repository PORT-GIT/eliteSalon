from django.db import models

# Create your models here.
class services(models.Model):
    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    category = models.CharField(null=False, max_length=25)
    serviceName = models.CharField(null=False, max_length=25)
    price = models.IntegerField(null=False)
    description = models.TextField(null=False, max_length=100)
    durationOfService = models.CharField(null=False, max_length=20)
    updatedAt = models.DateTimeField(auto_now=True)

class salonAppointment(models.Model):
    APPOINTMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    customerId = models.ForeignKey('users.customerProfile', on_delete=models.CASCADE)
    serviceId = models.ForeignKey(services, on_delete=models.SET_NULL, null=True)
    employeeId = models.ForeignKey('users.employeeProfile', on_delete=models.CASCADE)
    scheduleDay = models.DateField()
    appointmentStatus = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='PENDING')
    startTime = models.TimeField()
    endTime = models.TimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class servicesGiven(models.Model):
    RATINGS = (
    ('1','1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    )

    id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
    salonAppointmentId = models.ForeignKey(salonAppointment, on_delete=models.SET_NULL, null=True)#sometimes a client cannot have an appointment  
    servicesGiven = models.ManyToManyField(services)
    customerId = models.ForeignKey('users.customerProfile',  on_delete=models.CASCADE)
    employeeId = models.ForeignKey('users.employeeProfile',  on_delete=models.CASCADE)
    customerRating = models.CharField(max_length=20, choices=RATINGS, default='1')
    customerComment = models.TextField(null=False)
    employeeRating = models.CharField(max_length=20, choices=RATINGS, default='1')
    employeeComment = models.TextField(null=False)