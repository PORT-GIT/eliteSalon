from django.contrib import admin
from .models import CustomerProfile, EmployeeProfile, AdminProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    can_delete = False #this prevents deleting instance in the admin panel
    max_num = 1 #show one instance only
    extra = 0 #will not show any extra form fields
# this is a base inline class for all profiles

class AdminProfileInline(ProfileInline):
    model = AdminProfile
    
class EmployeeProfileInline(ProfileInline):
    model = EmployeeProfile
    filter_horizontal = ('services_to_offer',)#this will handle the many2many field

class CustomerProfileInline(ProfileInline):
    model = CustomerProfile

# this will be used to override the default USERADMIN
class UserProfileAdmin(UserAdmin):
    inlines = []
    list_display = ('username', 'email', 'date_joined', 'role')

    # this adds a role column to the list of users in the admin panel
    # this will enable Django to look at the roles in the user profiles and show their role
    def role(self, obj):
        if hasattr(obj, 'admin_profile'):
            return "Admin"
        
        elif hasattr(obj, 'employee_profile'):
            return "Employee"
        
        elif hasattr(obj, 'customer_profile'):
            return "Customer"
        
        return "None"
    role.short_description = 'Role'

    def get_inlines(self, request, obj=None):
        if obj:
            if hasattr(obj, 'admin_profile'):
                return [AdminProfileInline]
            
            elif hasattr(obj, 'employee_profile'):
                return [EmployeeProfileInline]
            
            elif hasattr(obj, 'customer_profile'):
                return [CustomerProfileInline]
        return []


# this unregisters the default admin page for the built-in USER model
# and replaces it with the custom USERPROFILEADMIN that i have made
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
