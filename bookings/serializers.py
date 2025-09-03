from rest_framework import serializers
from .models import Booking
from accounts.models import CustomUser

class BookingSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'client', 'staff', 'service', 'appointment_time', 'status']
        extra_kwargs = {
            'staff': {'help_text': 'Staff user ID (CustomUser with role="staff")'}
        }

