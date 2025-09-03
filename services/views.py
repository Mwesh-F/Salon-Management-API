from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from staff.authentication import StaffTokenAuthentication
from .models import Service
from .serializers import ServiceSerializer

# Permission for staff
class IsStaff(BasePermission):
	def has_permission(self, request, view):
		from staff.models import Staff
		return isinstance(request.user, Staff)

class ServiceListCreateView(generics.ListCreateAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	authentication_classes = [TokenAuthentication, StaffTokenAuthentication]
	permission_classes = [IsAuthenticated]


# Retrieve, update, delete services (any authenticated user)
class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	authentication_classes = [TokenAuthentication, StaffTokenAuthentication]
	permission_classes = [IsAuthenticated]
