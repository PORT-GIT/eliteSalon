from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import customerProfile, employeeProfile, adminProfile, customUser

# Register your models here.
admin.site.register(customerProfile)
admin.site.register(employeeProfile)
admin.site.register(adminProfile)


#this is how to custom users are properly registered
class customUserAdmin(UserAdmin):
    model = customUser
    list_display = ('username', 'email', 'phoneNumber')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)

admin.site.register(customUser, customUserAdmin)

