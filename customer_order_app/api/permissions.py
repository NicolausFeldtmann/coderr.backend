from rest_framework.permissions import IsAuthenticated, BasePermission
from user_auth_app.models import UserProfile

class IsCustomer(IsAuthenticated):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.role == 'customer'
        except UserProfile.DoesNotExist:
            return False