
from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer

# Custom permission so only the client can update or delete their booking
class IsBookingOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.client == request.user

# List all bookings and create a new booking

# List all bookings and create a new booking, with filtering
class BookingListCreateView(generics.ListCreateAPIView):
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		queryset = Booking.objects.all()
		status = self.request.query_params.get('status')
		staff = self.request.query_params.get('staff')
		service = self.request.query_params.get('service')
		appointment_time = self.request.query_params.get('appointment_time')

		if status:
			queryset = queryset.filter(status=status)
		if staff:
			queryset = queryset.filter(staff_id=staff)
		if service:
			queryset = queryset.filter(service_id=service)
		if appointment_time:
			queryset = queryset.filter(appointment_time=appointment_time)
		return queryset

	def perform_create(self, serializer):
		serializer.save(client=self.request.user)

# Retrieve, update, and delete/cancel a booking

from django.utils import timezone
from datetime import timedelta

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated, IsBookingOwner]

	def perform_update(self, serializer):
		old_status = self.get_object().status
		booking = serializer.save()
		# If status changed to completed, create a new booking 6 weeks later
		if old_status != 'completed' and booking.status == 'completed':
			new_appointment_time = booking.appointment_time + timedelta(weeks=6)
			Booking.objects.create(
				client=booking.client,
				staff=booking.staff,
				service=booking.service,
				appointment_time=new_appointment_time,
				status='pending'
			)
