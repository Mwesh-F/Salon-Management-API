
from rest_framework import serializers
from .models import Staff

# Serializer for staff registration
class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Staff
        fields = ['username', 'email', 'password']

# Serializer for staff login
class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# General staff serializer (for listing, etc.)
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'username', 'email', 'password']
