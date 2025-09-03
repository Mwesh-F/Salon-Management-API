from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from services.models import Service
from bookings.models import Booking
 # from staff.models import Staff  # Deprecated

class StaffCreationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='admin', email='admin@example.com', password='adminpass')
        self.client.force_authenticate(user=self.user)

    def test_create_staff(self):
        url = reverse('register')
        data = {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123',
            'role': 'staff'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'staff1')
        self.assertEqual(response.data['role'], 'staff')

class StaffLoginTest(APITestCase):
    def setUp(self):
        self.staff = CustomUser.objects.create_user(username='staff1', email='staff1@example.com', password='staffpass123', role='staff')

    def test_staff_login(self):
        url = reverse('login')
        data = {
            'username': 'staff1',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from services.models import Service
from bookings.models import Booking
from staff.models import Staff
class StaffCreationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='admin', email='admin@example.com', password='adminpass')
        self.client.force_authenticate(user=self.user)

    def test_create_staff(self):
        url = reverse('staff-list-create')
        data = {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'staff1')

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')

class ServiceCreationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_create_service(self):
        url = reverse('service-list-create')
        data = {
            'name': 'Haircut',
            'description': 'Basic haircut',
            'due_date': '2025-09-01T10:00:00Z',
            'priority_level': 'Low'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Haircut')

class BookingTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)
        self.service = Service.objects.create(name='Massage', description='Relaxing massage', due_date='2025-09-01T11:00:00Z', priority_level='Medium')

    def test_create_booking(self):
        url = reverse('booking-list-create')
        data = {
            'service': self.service.id,
            'appointment_time': '2025-09-02T12:00:00Z',
            'status': 'pending'
        }
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print('Booking creation error:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['service'], self.service.id)

    def test_update_and_cancel_booking(self):
        booking = Booking.objects.create(client=self.user, service=self.service, appointment_time='2025-09-02T12:00:00Z', status='pending')
        url = reverse('booking-detail', args=[booking.id])
        # Update status to confirmed
        response = self.client.patch(url, {'status': 'confirmed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'confirmed')
        # Cancel booking
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
