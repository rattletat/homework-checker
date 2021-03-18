import os
from django.shortcuts import reverse

from rest_framework import serializers

from ..models import Lecture, Lesson


class LectureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["title", "slug", "start", "end"]
        ordering = ["end", "start", "title"]


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

    def get_lessons(self, obj):
        lessons = obj.lessons.order_by('title')
        return LessonListSerializer(lessons, many=True).data

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
            obj.resources.order_by("title"),
        )


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end"]
        ordering = ["title"]


class LessonDetailSerializer(serializers.ModelSerializer):
    resources = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = ["slug", "title", "start", "end", "description", "resources"]
        ordering = ["title"]

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
            obj.resources.order_by("title"),
        )


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["participants"]
