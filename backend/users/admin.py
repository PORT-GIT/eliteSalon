from django.contrib import admin
from .models import CustomerProfile, EmployeeProfile, AdminProfile
from django.contrib.auth.models import User

class AdminRegister(admin.ModelAdmin):
    list_display = ('id', 'user_profile')

admin.site.register(AdminProfile, AdminRegister)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile')
    filter_horizontal = ('services_to_offer',)

admin.site.register(EmployeeProfile, EmployeeAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile')

admin.site.register(CustomerProfile, CustomerAdmin)