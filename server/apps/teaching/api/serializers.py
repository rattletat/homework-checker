from ..models import Lecture, Lesson
from rest_framework.response import Response
from rest_framework import serializers


class LectureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["title", "slug", "start", "end"]
        ordering = ["-start"]


class LectureDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True)
    registered = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lecture
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "start",
            "end",
            "lessons",
            "registered",
        ]
        ordering = ["-start"]

    def get_lessons(self, obj):
        return LessonListSerializer(obj.lessons, many=True).data

    def get_registered(self, obj):
        user = serializers.CurrentUserDefault()
        return user in obj.participants.all()


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end"]
        ordering = ["-start"]


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end", "description"]
        ordering = ["-start"]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["participants"]
