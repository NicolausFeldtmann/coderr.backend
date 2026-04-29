from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == "DELETE":
            return request.method.user.is_superuser

        return request.user == obj.user or request.user.is_superuser