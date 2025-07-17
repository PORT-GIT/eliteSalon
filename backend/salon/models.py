# from django.db import models

# # Create your models here.
# class service(models.Model):
#     id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
#     category = models.CharField(null=False, max_length=25)
#     service_name = models.CharField(null=False, max_length=25,unique=True)
#     price = models.IntegerField(null=False)
#     description = models.TextField(null=False, max_length=400)
#     durationOfService = models.CharField(null=False, max_length=20)
#     createdAt = models.DateField(auto_now_add=True)
#     updatedAt = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = 'services'

#     def __str__(self):
#         return self.service_name

# class salonAppointment(models.Model):
#     APPOINTMENT_STATUS = (
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#     )

#     id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
#     customerId = models.ForeignKey('users.customerProfile', on_delete=models.CASCADE)
#     services = models.ManyToManyField(service, related_name="salon_appointment")
#     employeeId = models.ForeignKey('users.employeeProfile', on_delete=models.CASCADE)
#     scheduleDay = models.DateField()
#     appointmentStatus = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='PENDING')
#     startTime = models.TimeField()
#     endTime = models.TimeField()
#     createdAt = models.DateTimeField(auto_now_add=True)
#     updatedAt = models.DateTimeField(auto_now=True)

    
#     def __str__(self):
#      return f"{self.id} - {self.customerId} - {self.employeeId} - {self.scheduleDay}"

# class servicesGiven(models.Model):
#     RATINGS = (
#     ('1','1'),
#     ('2', '2'),
#     ('3', '3'),
#     ('4', '4'),
#     ('5', '5'),
#     )

#     id = models.AutoField(primary_key=True)#this will enable the auto-increment factor
#     salonAppointmentId = models.ForeignKey(salonAppointment, on_delete=models.SET_NULL, null=True, to_field='id')#sometimes a client cannot have an appointment  
#     servicesId = models.ForeignKey(service, to_field='id', on_delete=models.CASCADE)
#     customerId = models.ForeignKey('users.customerProfile',  on_delete=models.CASCADE, to_field='id')
#     employeeId = models.ForeignKey('users.employeeProfile',  on_delete=models.CASCADE, to_field='id')
#     customerRating = models.IntegerField(choices=RATINGS)
#     customerComment = models.TextField(null=False, max_length=200)
#     employeeRating = models.IntegerField(choices=RATINGS)
#     employeeComment = models.TextField(null=False, max_length=200)

#     def __str__(self):
#         return self.salonAppointmentId