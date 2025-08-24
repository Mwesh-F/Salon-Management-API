
from django.db import models

class Service(models.Model):
	LOW = 'Low'
	MEDIUM = 'Medium'
	HIGH = 'High'
	PRIORITY_CHOICES = [
		(LOW, 'Low'),
		(MEDIUM, 'Medium'),
		(HIGH, 'High'),
	]

	name = models.CharField(max_length=255)
	description = models.TextField()
	due_date = models.DateTimeField()
	priority_level = models.CharField(max_length=6, choices=PRIORITY_CHOICES)

	def __str__(self):
		return self.name
