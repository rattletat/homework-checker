from rest_framework import permissions
from ..models import Submission


class isAuthor(permissions.BasePermission):
    """
    Gives permission to users that created the submission.
    Admins can see all content.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous:
            return False
        if user.is_staff:
            return True

        if isinstance(obj, Submission):
            return obj.user == user
