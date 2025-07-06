from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, adminProfile, employeeProfile, customerProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'ADMIN':
            adminProfile.objects.create(user=instance)
        elif instance.role == 'EMPLOYEE':
            employeeProfile.objects.create(user=instance)
        elif instance.role == 'CUSTOMER':
            customerProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.role == 'ADMIN':
            instance.admin_profile.save()
        elif instance.role == 'EMPLOYEE':
            instance.employee_profile.save()
        elif instance.role == 'CUSTOMER':
            instance.customer_profile.save()
    except:
        # handles case where profile doesn't exist yet
        pass