from django.urls import path
from .views import StaffListCreateView, StaffUpdateDeleteView

urlpatterns = [
    path('staff/', StaffListCreateView.as_view(), name='staff-list-create'),
    path('staff/<int:pk>/', StaffUpdateDeleteView.as_view(), name='staff-update-delete'),
]
