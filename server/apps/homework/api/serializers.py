from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Exercise, Submission
from ..validators import FileValidator

FILETYPE_SPECIFICS = {
    Exercise.ProgrammingLanguages.PYTHON: {
        "allowed_mimetypes": ["text/x-python", "text/plain"],
        "allowed_extensions": ["py"],
    },
    Exercise.ProgrammingLanguages.R: {
        "allowed_mimetypes": ["text/plain"],
        "allowed_extensions": ["r"],
    },
}


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "title", "description", "max_score"]
        order = ["title"]


class SubmissionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = data["user"]
        exercise = data["exercise"]
        lesson = exercise.lesson

        # Check type, extension and size of file
        file_validator = FileValidator(
            min_size=exercise.min_upload_size,
            max_size=exercise.max_upload_size,
            **FILETYPE_SPECIFICS[exercise.programming_language]
        )
        file_validator(data["file"])

        # Check if user is registered for course
        if lesson.lecture not in user.enrolled_lectures.all():
            raise serializers.ValidationError(
                "You are not registered for this lecture."
            )

        # Check timestamp of submission
        if lesson.start and now() < lesson.start:
            raise serializers.ValidationError(
                "You cannot upload a submission before the lesson has started."
            )
        if lesson.end and lesson.end < now():
            raise serializers.ValidationError(
                "You cannot upload a submission after the lesson has ended."
            )

        return data

    class Meta:
        model = Submission
        fields = ["exercise", "user", "file", "file_hash"]
        validators = [
            UniqueTogetherValidator(
                queryset=Submission.objects.all(),
                fields=["user", "file_hash", "exercise"],
                message=("You already uploaded this exact same file before!"),
            )
        ]


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "created", "score", "output"]
