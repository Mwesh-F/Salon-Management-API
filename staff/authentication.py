from rest_framework.authentication import BaseAuthentication
from staff.models import Staff

class StaffTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Token staff-') and auth_header.endswith('-token'):
            try:
                staff_id = int(auth_header.split('-')[1])
                staff = Staff.objects.get(id=staff_id)
                return (staff, None)
            except (ValueError, Staff.DoesNotExist):
                return None
        return None
