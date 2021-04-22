from rest_framework import permissions
from ..models import Lecture, Lesson, LectureResource, LessonResource
from apps.homework.models import Exercise


class IsEnrolled(permissions.BasePermission):
    """
    Custom permission to only allow enrolled students to see the lecture/ lesson.
    Admins can see all content.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous:
            return False
        if user.is_staff:
            return True

        if isinstance(obj, Lecture):
            return obj in user.enrolled_lectures.all()
        if isinstance(obj, (Lesson, LectureResource)):
            return obj.lecture in user.enrolled_lectures.all()
        if isinstance(obj, LessonResource, Exercise):
            return obj.lesson.lecture in user.enrolled_lectures.all()
        return user.is_staff


class IsNotWaiting(permissions.BasePermission):
    """
    Custom permission to only allow enrolled students to see the lecture/ lesson.
    Admins can see all content.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        print("USER: ", str(user.is_staff))
        if user.is_anonymous:
            return False
        if user.is_staff:
            return True

        if isinstance(obj, (Lecture, Lesson)):
            print("STATUS1: ", str(obj.status))
            print("VALUE: ", obj.status != "WAITING")
            return obj.status != "WAITING"
        if isinstance(obj, LectureResource):
            print("STATUS2: ", str(obj.lecture.status))
            return obj.lecture.status != "WAITING"
        if isinstance(obj, LessonResource, Exercise):
            print("STATUS3: ", str(obj.lesson.status))
            return obj.lesson.status != "WAITING"
