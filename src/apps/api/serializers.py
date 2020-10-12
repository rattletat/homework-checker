from apps.teaching.models import Lecture, Lesson
from rest_framework import serializers


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["id", "title", "slug"]


class LectureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["id", "title", "slug", "description"]


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    lecture = serializers.HyperlinkedRelatedField(
        view_name="api:lecture-detail", read_only=True
    )

    class Meta:
        model = Lesson
        fields = ["title", "id", "lecture"]
