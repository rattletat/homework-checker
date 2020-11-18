import os
from django.shortcuts import reverse

from rest_framework import serializers

from ..models import Lecture, Lesson


class LectureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["title", "slug", "start", "end"]
        ordering = ["title"]


class LectureDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True)
    resources = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lecture
        fields = [
            "title",
            "slug",
            "description",
            "start",
            "end",
            "lessons",
            "resources",
        ]
        ordering = ["-start"]

    def get_lessons(self, obj):
        return LessonListSerializer(obj.lessons, many=True).data

    def get_resources(self, obj):
        return map(
            lambda r: {
                "title": r.title,
                "filename": os.path.basename(r.file.name),
                "download_uri": reverse(
                    "api:lecture_download",
                    kwargs={"lecture_slug": obj.slug, "resource_id": r.id},
                ),
            },
            obj.resources.filter(public=True, listed=True),
        )


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end"]
        ordering = ["-start"]


class LessonDetailSerializer(serializers.ModelSerializer):
    resources = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end", "description", "resources"]
        ordering = ["-start"]

    def get_resources(self, obj):
        return map(
            lambda r: {
                "title": r.title,
                "filename": os.path.basename(r.file.name),
                "download_uri": reverse(
                    "api:lesson_download",
                    kwargs={
                        "lecture_slug": obj.lecture.slug,
                        "lesson_slug": obj.slug,
                        "resource_id": r.id,
                    },
                ),
            },
            obj.resources.filter(public=True, listed=True),
        )


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["participants"]
