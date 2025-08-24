
from rest_framework import generics
from .models import Staff
from .serializers import StaffSerializer

# List all staff and create new staff
class StaffListCreateView(generics.ListCreateAPIView):
	queryset = Staff.objects.all()
	serializer_class = StaffSerializer

# Update and delete staff
class StaffUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Staff.objects.all()
	serializer_class = StaffSerializer
