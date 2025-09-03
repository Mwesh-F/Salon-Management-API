from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from services.models import Service
from bookings.models import Booking

# Staff Service Update/Delete Test
class TestStaffServiceUpdateDelete(APITestCase):
    def setUp(self):
        # Register staff
        self.staff_reg_data = {
            'username': 'staff2',
            'email': 'staff2@example.com',
            'password': 'staffpass456'
        }
        self.client.post(reverse('staff-register'), self.staff_reg_data)
        # Login staff
        login_resp = self.client.post(reverse('staff-login'), {
            'username': 'staff2',
            'password': 'staffpass456'
        })
        self.token = login_resp.data.get('token')
        self.auth_header = {'HTTP_AUTHORIZATION': self.token}

        # Create a service
        self.service_data = {
            'name': 'Test Service',
            'description': 'Service for update/delete test',
            'due_date': '2025-09-01T10:00:00Z',
            'priority_level': 'Medium'
        }
        create_resp = self.client.post('/api/services/', self.service_data, **self.auth_header)
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        self.service_id = create_resp.data.get('id')

    def test_update_service(self):
        update_data = {'name': 'Updated Service', 'priority_level': 'High'}
        url = f'/api/services/{self.service_id}/'
        resp = self.client.patch(url, update_data, format='json', **self.auth_header)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Updated Service')
        self.assertEqual(resp.data['priority_level'], 'High')

    def test_delete_service(self):
        url = f'/api/services/{self.service_id}/'
        resp = self.client.delete(url, **self.auth_header)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from services.models import Service
from bookings.models import Booking

# Staff Tests
class TestStaffRegistration(APITestCase):
    def test_create_staff(self):
        url = reverse('staff-register')
        data = {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

class TestStaffLogin(APITestCase):
    def setUp(self):
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })

    def test_staff_login(self):
        url = reverse('staff-login')
        data = {
            'username': 'staff1',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

# User Registration Test
class TestUserRegistration(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')

# --- Service Tests ---
class TestServiceCreation(APITestCase):
    def setUp(self):
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })
        login_response = self.client.post(reverse('staff-login'), {
            'username': 'staff1',
            'password': 'staffpass123'
        })
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_service(self):
        url = reverse('service-list-create')
        data = {
            'name': 'Haircut',
            'description': 'Basic haircut',
            'due_date': '2025-09-01T10:00:00Z',
            'priority_level': 'Low'
        }
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            self.fail(f"Service creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Haircut')

# Booking Tests
class TestBooking(APITestCase):
    def setUp(self):
        # Create a user to act as client
        self.client_user = CustomUser.objects.create_user(username='clientuser', email='client@example.com', password='clientpass123')
        # Register and login staff
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })
        login_response = self.client.post(reverse('staff-login'), {
            'username': 'staff1',
            'password': 'staffpass123'
        })
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.service = Service.objects.create(name='Massage', description='Relaxing massage', due_date='2025-09-01T11:00:00Z', priority_level='Medium')

    def test_create_booking(self):
        url = reverse('booking-list-create')
        data = {
            'client': self.client_user.id,
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
        booking = Booking.objects.create(client=self.client_user, service=self.service, appointment_time='2025-09-02T12:00:00Z', status='pending')
        url = reverse('booking-detail', args=[booking.id])
        # Update status to confirmed
        response = self.client.patch(url, {'status': 'confirmed'})
        if response.status_code != status.HTTP_200_OK:
            self.fail(f"Booking update failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'confirmed')
        # Cancel booking
        response = self.client.delete(url)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            self.fail(f"Booking cancel failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Test staff registration using new endpoint
class TestStaffRegistration(APITestCase):
    def test_create_staff(self):
        url = reverse('staff-register')
        data = {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)


# Test staff login using new endpoint
class TestStaffLogin(APITestCase):
    def setUp(self):
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })

    def test_staff_login(self):
        url = reverse('staff-login')
        data = {
            'username': 'staff1',
            'password': 'staffpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')


# Test service creation with staff token
class TestServiceCreation(APITestCase):
    def setUp(self):
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })
        login_response = self.client.post(reverse('staff-login'), {
            'username': 'staff1',
            'password': 'staffpass123'
        })
        self.token = login_response.data['token']

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


# Test booking creation/update/cancel with staff token
class TestBooking(APITestCase):
    def setUp(self):
        self.client_user = CustomUser.objects.create_user(username='clientuser', email='client@example.com', password='clientpass123')
        self.client.post(reverse('staff-register'), {
            'username': 'staff1',
            'email': 'staff1@example.com',
            'password': 'staffpass123'
        })
        login_response = self.client.post(reverse('staff-login'), {
            'username': 'staff1',
            'password': 'staffpass123'
        })
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.service = Service.objects.create(name='Massage', description='Relaxing massage', due_date='2025-09-01T11:00:00Z', priority_level='Medium')

    def test_create_booking(self):
        url = reverse('booking-list-create')
        data = {
            'service': self.service.id,
            'appointment_time': '2025-09-02T12:00:00Z',
            'status': 'pending',
            'client': self.client_user.id
        }
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print('Booking creation error:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['service'], self.service.id)

    def test_update_and_cancel_booking(self):
        booking = Booking.objects.create(client=self.client_user, service=self.service, appointment_time='2025-09-02T12:00:00Z', status='pending')
        url = reverse('booking-detail', args=[booking.id])
        # Update status to confirmed
        response = self.client.patch(url, {'status': 'confirmed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'confirmed')
        # Cancel booking
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
