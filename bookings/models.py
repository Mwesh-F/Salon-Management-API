
from django.db import models
from accounts.models import CustomUser
 # from staff.models import Staff  # Deprecated
from services.models import Service

class Booking(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_CONFIRMED = 'confirmed'
	STATUS_COMPLETED = 'completed'
	STATUS_CANCELED = 'canceled'
	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_CONFIRMED, 'Confirmed'),
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_CANCELED, 'Canceled'),
	]

	client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_bookings')
	staff = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_bookings', limit_choices_to={'role': 'staff'})
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	appointment_time = models.DateTimeField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)

	def __str__(self):
		return f"Booking for {self.client.username} - {self.service.name} at {self.appointment_time}"
