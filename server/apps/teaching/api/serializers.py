import os

from apps.homework.models import Submission
from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import reverse
from django.utils.timezone import now
from rest_framework import serializers

from ..models import Lecture, Lesson


class EnrolledLectureListSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    next_deadline = serializers.SerializerMethodField()

    def get_score(self, lecture):
        user = self.context["request"].user
        return lecture.get_score(user)

    def get_grade(self, lecture):
        user = self.context["request"].user
        score = lecture.get_score(user)
        if scale := lecture.grading_scale:
            return scale.get_grade(score)

    def get_next_deadline(self, lecture):
        lesson = (
            lecture.lessons.filter(end__isnull=False, end__gt=now(), exercises__graded=True)
            .order_by("end")
            .first()
        )
        if lesson:
            return {"title": lesson.title, "end": lesson.end}

    class Meta:
        model = Lecture
        fields = ["title", "slug", "start", "end", "status", "score", "grade", "next_deadline"]
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
        lessons = obj.lessons.order_by("start", "title", "end")
        return LessonListSerializer(lessons, many=True, context=self.context).data

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
    user_score = serializers.SerializerMethodField()
    max_score = serializers.SerializerMethodField()

    def get_max_score(self, lesson):
        return lesson.exercises.filter(graded=True).aggregate(
            max=Coalesce(Sum("max_score"), 0)
        )["max"]

    def get_user_score(self, lesson):
        user = self.context["request"].user
        return lesson.get_score(user)

    class Meta:
        model = Lesson
        fields = ["slug", "title", "status", "start", "end", "max_score", "user_score"]
        ordering = ["start", "title", "end"]


class LessonScoreSerializer(serializers.ModelSerializer):
    highest_scores = serializers.SerializerMethodField()

    def get_highest_scores(self, obj):
        user = self.context["request"].user
        return {
            str(exercise.id): Submission.objects.filter(exercise=exercise, user=user).aggregate(
                max=Coalesce(Max("score"), 0)
            )["max"]
            for exercise in obj.exercises.all()
        }

    class Meta:
        model = Lesson
        fields = ["highest_scores"]


class LessonDetailSerializer(serializers.ModelSerializer):
    resources = serializers.SerializerMethodField()

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
