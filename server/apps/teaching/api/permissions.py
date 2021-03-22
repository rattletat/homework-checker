from rest_framework import permissions
from ..models import Lecture, Lesson, LectureResource, LessonResource


class IsEnrolled(permissions.BasePermission):
    """
    Custom permission to only allow enrolled students to see the lecture/ lesson.
    Admins can see all content.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.isstaff:
            return True

        if isinstance(obj, Lecture):
            return obj in user.enrolled_lectures
        if isinstance(obj, [Lesson, LectureResource]):
            return obj.lecture in user.enrolled_lectures
        if isinstance(obj, LessonResource):
            return obj.lesson.lecture in user.enrolled_lectures
        return False
