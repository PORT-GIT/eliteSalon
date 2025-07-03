from django.contrib import admin
from .models import services, salonAppointment, servicesGiven

# Register your models here.
admin.site.register(services)
admin.site.register (salonAppointment)
admin.site.register (servicesGiven)
