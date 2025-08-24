
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer, LoginSerializer, LogoutSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
	serializer_class = UserRegistrationSerializer
	permission_classes = [AllowAny]

class LoginView(APIView):
	permission_classes = [AllowAny]
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		username = serializer.validated_data['username']
		password = serializer.validated_data['password']
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			token, created = Token.objects.get_or_create(user=user)
			return Response({'token': token.key}, status=status.HTTP_200_OK)
		return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_class = LogoutSerializer

	def post(self, request):
		request.user.auth_token.delete()
		logout(request)
		return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)
