from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

User = get_user_model()

class PatientProfile(models.Model):
  """Patient-specific profile information"""
  GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ('prefer_not_to_say', 'Prefer not to say')
  ]

  BLOOD_TYPE_CHOICES = [
    ('A+', 'A Positive'),
    ('A-','A Negative'),
    ('B+','B Positive'),
    ('B-','B Negative'),
    ('AB+','AB Positive'),
    ('AB-','AB Negative'),
    ('O+','O Positive'),
    ('O-','O Negative'),
    ('unknown', 'Unknown')
  ]

  id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, 
                              related_name='patient_profile', limit_choices_to={'role':'patient'})

