from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, full_name, email, password=None, is_active=False, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            is_active=is_active,
            role = extra_fields.get('role'),
            phone_number = extra_fields.get('phone')
        )

        user.set_password(password)
        user.is_active = True
        #set password in built for password
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            #normalize email makes capital email small
            password = password,
            full_name = full_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    user_roles=(
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    )
    full_name      = models.CharField(max_length=50, null=True, blank=True)
    username        = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email           = models.EmailField(max_length=300, unique=True)
    phone_number    = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length = 10, choices=user_roles, null=True, blank=True)
# required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #using email for login
    REQUIRED_FIELDS = ['full_name']

    objects = MyAccountManager()
    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

