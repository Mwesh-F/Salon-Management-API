from django.urls import path
from .views import StaffRegistrationView, StaffLoginView

urlpatterns = [
	path('register/', StaffRegistrationView.as_view(), name='staff-register'),
	path('login/', StaffLoginView.as_view(), name='staff-login'),
]