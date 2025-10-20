from rest_framework.permissions import BasePermission

class IsAdminOrStaff(BasePermission):
    """
    Custom permission to allow access only to users in the Admin or Staff groups.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if the user belongs to the Admin or Staff group
        return request.user.groups.filter(name__in=['Admin', 'Staff']).exists() or request.user.is_superuser
