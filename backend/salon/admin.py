from django.contrib import admin
from .models import service, salonAppointment, servicesGiven

# Register your models here.

class serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'category', 'createdAt')

admin.site.register(service, serviceAdmin)

class appointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customerId', 'employeeId', 'scheduleDay', 'appointmentTime', 'appointmentEndTime', 'createdAt')
    filter_horizontal = ('services',)#handles many-to-many fields

admin.site.register (salonAppointment, appointmentAdmin)

class serviceGivenAdmin(admin.ModelAdmin):
    list_display = ('id', 'salonAppointmentId', 'servicesId', 'customerRating')
    
admin.site.register (servicesGiven, serviceGivenAdmin)
