from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import  BaseUserManager
from django.utils.translation import gettext_lazy as _

# the need for the custom manager is solely because of the switch to email-based authentication
# this will modify user and superuser creation
# it will handle superuser creation differently
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        
        if not role:
            raise ValueError(_('The user role must be specified')) 
        
        if not email:
            raise ValueError(_('The email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(role=role, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # this will use the current database
        return user
    
    def create_superuser(self, email, password, role, **extra_fields):
        # the superuser will be created and saved with the given email, password and role. 
        # extra fields are added to indicate that the user is staff, active, and indeed a superuser.

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # this will validate staff/superuser flags
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        
        return self.create_user(email, password, role, **extra_fields)

class CustomUser(AbstractUser):
    #from the django file the abstractuser has the following fields username, first and last name, email, date joined, is staff, is active etc

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EMPLOYEE', 'Employee'),
        ('CUSTOMER', 'Customer'),
    )

    username = None #i can use user emails as way to create unique profiles for them rather than a username that has validation
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('user role'),choices=ROLE_CHOICES, null=False, blank=False, max_length=20)
    # this is when the user verifies their email
    # is_verified = models.BooleanField(_('verified'), default=False)
    # verification_token = models.CharField(_('verification token'), max_length=100, blank=True, null=True)# the blank allows unverified users

    # since i am changing the USERNAME_FIELD TO email then I will need to create a custom manager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    # the email and password fields are not added to the REQUIRED_FIELDS 
    # because they are added by default on a deeper layer
    # The REQUIRED_FIELDS are a list of the field names that will be prompted
    #  for when creating a user via the createsuperuser management command.

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class adminProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    phone_number = models.CharField(null=False, max_length=25)

    def __str__(self):
        return f"{self.user.email}'s Admin Profile"
    

class employeeProfile(models.Model):
    WORK_STATUS = (
        ('FREE', 'Free'),
        ('BUSY', 'Busy'),
        ('BREAK', 'At break')
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee_profile")
    phone_number = models.CharField(null=False, max_length=25)
    date_of_birth = models.DateField(null=False, blank=False)
    skills = models.CharField(null=False, max_length=200, blank=False)
    services_offered = models.ForeignKey('salon.service', verbose_name=_('services offered'), on_delete=models.CASCADE)
    #this shows the one-many relationship between the employee an the services they offer
    work_status = models.CharField(choices=WORK_STATUS, max_length=20, default='FREE')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Employee Profile"


class customerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(null=False, max_length=25)
    date_of_birth = models.DateField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Customer Profile"

