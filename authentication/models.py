from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid

class UserManager(BaseUserManager):
  def create_user(self, email, password = None, **extra_fields):
    if not email:
      raise ValueError('The email field must be set')
    
    email = self.normalize_email(email)
    user = self.model(email = email, **extra_fields)
    user.set_password(password)
    user.save(using = self._db)
    return user
  
  def create_superuser(self, email, password = None, **extra_fields):
    extra_fields.setdefault(key = 'is_staff',default = True)
    extra_fields.setdefault(key = 'is_superuser', default = True)
    extra_fields.setdefault(key = 'role', default = 'admin')
    return self.create_user(email, password, **extra_fields)
  
  def get_patients(self):
    return self.filter(role = 'patient', is_active = True)

  def get_consultants(self):
    return self.filter(role = 'consultant', is_active = True)

class User(AbstractBaseUser, PermissionsMixin):
  ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('consultant', 'Consultant'),
    ('admin', 'Admin')
  ]
