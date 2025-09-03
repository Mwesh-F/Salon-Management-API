from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Staff
from .serializers import StaffRegistrationSerializer, StaffLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# Simple in-memory token store for demo (use a DB or cache for production)
staff_tokens = {}

class StaffRegistrationView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		serializer = StaffRegistrationSerializer(data=request.data)
		if serializer.is_valid():
			staff = serializer.save()
			return Response({'message': 'Staff registered successfully'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffLoginView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		serializer = StaffLoginSerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.validated_data['username']
			password = serializer.validated_data['password']
			try:
				staff = Staff.objects.get(username=username)
				if staff.password == password:
					# Generate a simple token
					token = f'staff-{staff.id}-token'
					staff_tokens[staff.id] = token
					return Response({'token': token}, status=status.HTTP_200_OK)
				else:
					return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
			except Staff.DoesNotExist:
				return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
