from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
# Custom User Manager
class UserManager (BaseUserManager):
    def create_user(self, email, full_name, password = None, **extra_fields):
        if not email:
            raise ValueError("Email Field is Must be Required")
        email = self.normalize_email(email)
        user = self.model(email = email, full_name = full_name, **extra_fields )
        user.set_password(password)
        user.otp = str(random.randint(100000, 999999)) #generate 6 digit otp
        user.save(using = self._db)
        return user
    def create_superuser(self, email, full_name, password = None, **extra_fields ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError("SuperUser Must Have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser Must Have is_superuser=True")
        return self.create_user(email, full_name, password, **extra_fields)
    


#Custom User Model
class UserModel(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique = True)
    full_name = models.CharField(max_length = 200)
    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, default = 'user')
    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    otp = models.CharField(max_length = 6, blank = True, null = True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.email} ({self.role})"
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

#Signal
class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ManyToManyField(Employee, related_name='test', blank= True, null = True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
@receiver(m2m_changed, sender = Test.assigned_to.through)
def test_signal_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print( instance, instance.assigned_to.all())
        assinged_emails = [emp.email for emp in instance.assigned_to.all()]
        print('Cheking...', assinged_emails)

        send_mail(
            "New task Assigned",
            f"You Have been Assigned to the Task :{instance.title}",
            "fardinazim7@gmail.com",
            assinged_emails,
            fail_silently=False,
    )




