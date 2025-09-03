
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	ROLE_CHOICES = (
		('client', 'Client'),
		('staff', 'Staff'),
		('admin', 'Admin'),
	)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'username'

	def __str__(self):
		return f"{self.username} ({self.role})"
