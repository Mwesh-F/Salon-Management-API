# Staff model for authentication
from django.db import models

class Staff(models.Model):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)

	def __str__(self):
		return self.username

	@property
	def is_authenticated(self):
		return True

