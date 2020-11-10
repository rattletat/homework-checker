from ..models import Exercise, Submission
from rest_framework import serializers


class ExerciseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "title", "slug", "description", "max_score", "start", "end"]


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    lesson = serializers.HyperlinkedRelatedField(
        view_name="api:lesson-detail", read_only=True
    )

    class Meta:
        model = Exercise
        fields = ["id", "title", "lesson"]


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "exercise", "score", "output", "created"]
