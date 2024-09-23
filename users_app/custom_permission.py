from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission to handle access for regular and admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Allow GET requests
            return True  # All users can read
        elif request.method in ['POST', 'PUT', 'PATCH']:
            return request.user.is_authenticated
        
        elif request.method == 'DELETE':  # Allow delete requests
            return request.user.is_superuser  # Only admin can delete
        return False
