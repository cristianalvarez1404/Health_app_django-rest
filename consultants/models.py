from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Speciality(models.Model):
  """Medical specialities"""
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)
  icon = models.CharField(max_length=50, blank=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_plural_name = 'Specialties'
    db_table = 'specialities'
    ordering = ['name']

  def __str__(self):
    return self.name
  
class ConsultantProfile(models.Model):
  """Consultant-specific profile information"""
  CONSULTATION_TYPE_CHOICES = [
    ('video','Video Consultation'),
    ('audio','Audio Only'),
    ('chat','Text Chat'),
    ('all','All Types')
  ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant_profile', limit_choices_to={'role': 'consultant'})
  speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT, related_name='consultants')
  avatar = models.ImageField(upload_to='consultants/avatars/', blank=True, null= True)
  bio = models.TextField(max_length=1000, blank=True)
  years_of_experience = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(50)])
  license_number = models.CharField(max_length=100, unique=True)
  medical_degree = models.CharField(max_length=200, blank=True)
  board_certifications = models.JSONField(default=list, blank=True)
  additional_qualifications = models.JSONField(default=True, blank=True)
  phone_regex = RegexValidator(regex= r'^\+?1?\d{9,15}$', message="Phone number must to be entered in format: '+99999999' . Up to 15 digits allowed.")
  phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
  clinic_name = models.CharField(max_length=200, blank=True)
  clinic_address = models.TextField(max_length=300, blank=True)
  clinic_city = models.CharField(max_length=100, blank=True)
  clinic_country = models.CharField(max_length=100, blank=True)
  consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0)])
  consultation_duration = models.PositiveIntegerField(default=30,help_text="Default consultation duration in minutes")
  consultation_types = models.CharField(max_length=10, choices=CONSULTATION_TYPE_CHOICES, default='all')
  languages_spoken = models.JSONField(default=list, blank=True)
  is_available = models.BooleanField(default=True)
  availability_schedule = models.JSONField(default=dict, blank=True, help_text="Weekly schedule with time slots")
  rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(5)])
  total_consultations = models.PositiveIntegerField(default=0)
  total_reviews = models.PositiveIntegerField(default=0)
  is_verified = models.BooleanField(default=False)
  verification_date = models.DateTimeField(blank=True, null = True)
  is_featured = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'consultant_profiles'
    verbose_name = 'Consultant Profile'
    verbose_name_plural = 'Consultant Profiles'
    indexes = [
      models.Index(fields=['user']),
      models.Index(fields=['speciality']),
      models.Index(fields=['is_verified', 'is_available']),
      models.Index(fields=['created_at']),
      models.Index(fields=['rating']),
    ]

  def __str__(self):
    return f"Dr. {self.user.full_name} - {self.speciality.name}"
  
  @property
  def avatar_url(self):
    if self.avatar:
      return self.avatar.url
    return None
  
  def verify_consultant(self):
    """Mark consultant as verified"""
    self.is_verified = True
    self.verification_date = timezone.now()
    self.save(update_fields=['is_verified','verification_date'])

  def update_rating(self):
    from django.db.models import Avg
    avg_rating = self.reviews_aggregate(Avg('rating'))['rating_avg']

    if avg_rating:
      self.rating = round(avg_rating, 2)
      self.save(update_fields=['rating'])

  def clean(self):
    if self.user and self.user.role != 'consultant':
      from django.core.exceptions import ValidationError
      raise ValidationError("User must have 'consultant' role")
    




