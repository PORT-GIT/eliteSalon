from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, customerProfile, employeeProfile, adminProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm, EmployeeRegistrationForm
# rather than use separate admin i will use INLINES
# also some fields are in CustomUser model
# Using inlines will allow me to view a user and the associated profile
class customerProfileInline(admin.StackedInline):
    model = customerProfile
    can_delete = False
    extra = 0
    max_num = 1
    #  can_delete=False and max_num=1 to enforce one profile per user
    verbose_name = 'Customer Profile'
    fields = ('phone_number', 'date_of_birth')

class employeeProfileInline(admin.StackedInline):
    model = employeeProfile
    form = EmployeeRegistrationForm
    can_delete = False
    extra = 0
    max_num = 1
    #  can_delete=False and max_num=1 to enforce one profile per user
    verbose_name = 'Employee Profile'
    fields = ('phone_number', 'work_status', 'date_of_birth', 'services_to_offer')
   
class adminProfileInline(admin.StackedInline):
    model = adminProfile
    can_delete = False
    extra = 0
    max_num = 1
    #  can_delete=False and max_num=1 to enforce one profile per user
    verbose_name = 'Admin Profile'
    fields = ('phone_number',)

##this is how to custom users are properly registered
class customUserAdmin(UserAdmin):
    # The list_display, list_filter, search_fields, and ordering properties 
    # specify what you see on the admin site when you click the 'Users' link.
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'role', 'is_staff', 'is_active')
    # IS_STAFF-"Designates whether the user can log into this admin site
    # IS_ACTIVE-Designates whether this user should be treated as active. "
        # "Unselect this instead of deleting accounts

    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',' first_name', 'last_name')
    ordering = ('-date_joined',)#this will call on the newest first
    readonly_fields = ('date_joined',) #this makes date_joined read-only

    # The fieldsets determine which properties are shown when you open details for existing users
    #  add_fieldsets properties determine which properties are shown when you add a user.

    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

        ('Important Dates',  {'fields': ('date_joined',)}),
    )

    #fields for creating new users
    add_fieldsets = (
        (None, { 'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}),
    )

    # this conditionally shows the profile inlines based on user role
    def get_inlines(self, request, obj=None):
        if obj:  # only for existing objects
            if obj.role == 'ADMIN':
                return [adminProfileInline]
            elif obj.role == 'EMPLOYEE':
                return [employeeProfileInline]
            elif obj.role == 'CUSTOMER':
                return [customerProfileInline]
        return []
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # I have defined custom forms like CustomUserCreationForm and CustomUserChangeForm 
    # to customize how user creation and modification is handled in the Django admin interface.

    #  the default forms UserCreationForm and UserChangeForm won’t know about my new fields therefore i have created a subclass that tells Django 
    # which model to use (CustomUser) and what fields to display.
    
admin.site.register(CustomUser, customUserAdmin)
