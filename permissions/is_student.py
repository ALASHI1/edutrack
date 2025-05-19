from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to users with an associated StudentProfile.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'studentprofile')
