
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)

	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'username'

	def __str__(self):
		return self.username
