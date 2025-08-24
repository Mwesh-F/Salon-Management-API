
from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer

# Custom permission so only the client can update or delete their booking
class IsBookingOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.client == request.user

# List all bookings and create a new booking
class BookingListCreateView(generics.ListCreateAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(client=self.request.user)

# Retrieve, update, and delete/cancel a booking
class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated, IsBookingOwner]
