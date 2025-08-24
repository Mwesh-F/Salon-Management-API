from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import Booking
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminders to clients 24 hours before their appointment.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        soon = now + timedelta(hours=24)
        bookings = Booking.objects.filter(appointment_time__gte=now, appointment_time__lte=soon, status='confirmed')
        if not bookings:
            self.stdout.write('No reminders to send.')
        for booking in bookings:
            client_email = booking.client.email
            appointment = booking.appointment_time.strftime('%Y-%m-%d %H:%M')
            service = booking.service.name
            self.stdout.write(f"Reminder: Email to {client_email} - You have a '{service}' appointment on {appointment}.")
