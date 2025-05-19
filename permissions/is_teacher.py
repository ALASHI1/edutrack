from rest_framework.permissions import BasePermission
from apps.accounts.models import TeacherProfile

class IsTeacher(BasePermission):
    """
    Allows access only to users with an associated TeacherProfile.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'teacherprofile')
