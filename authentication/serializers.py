from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only = True, min_length = 8)
  password_confirm = serializers.CharField(write_only = True)

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'role', 'password_confirm']

  def validate(self, attrs):
    if attrs['password'] != attrs['password_confirm']:
      raise serializers.ValidationError("passwords don't match")
    return attrs
  
  def create(self, validated_data):
    validated_data.pop('password_confirm')
    return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
  full_name = serializers.ReadOnlyField()
  has_verified_email = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = [
      'id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'is_online', 'last_seen', 'is_active', 'is_verified', 'has_verified_email', 'email_verified_at', 'created_at', 'updated_at'
    ]  

  
