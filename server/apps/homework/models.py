from apps.teaching.models import Lesson
from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel

from .helpers import get_exercise_rsc_path, get_submission_path, get_tests_path
from .storage import OverwriteStorage


class Exercise(UUIDModel):
    class ProgrammingLanguages(models.TextChoices):
        PYTHON = "py", "Python"
        R = "r", "R"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=255, populate_from="title")
    description = models.TextField(blank=True)
    max_score = models.PositiveSmallIntegerField()
    tests = models.FileField(
        storage=OverwriteStorage(), upload_to=get_tests_path, max_length=255
    )
    min_upload_size = models.PositiveIntegerField(
        "Minimal byte size",
        default=30,
    )
    max_upload_size = models.PositiveIntegerField(
        "Maximal byte size", default=5000
    )
    timeout = models.PositiveSmallIntegerField(
        "Timeout in seconds",
        default=10,
        )
    programming_language = models.CharField(
        max_length=2, choices=ProgrammingLanguages.choices
    )
    rated = models.BooleanField("Graded", default=True)

    def __str__(self):
        return f"{self.lesson} ({self.title})"

    class Meta:
        ordering = ["title"]


class Submission(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    file = models.FileField(upload_to=get_submission_path, max_length=255)
    file_hash = models.CharField(max_length=40)
    score = models.PositiveSmallIntegerField(default=0)
    output = models.TextField(blank=True)

    def __str__(self):
        if self.score:
            return f"{self.user} ({self.exercise.title} - {self.score}/{self.exercise.max_score})"
        else:
            return f"{self.user} ({self.exercise.title} - pending)"

    class Meta:
        unique_together = (
            "file_hash",
            "user",
            "exercise",
        )


class ExerciseResource(UUIDModel, TimeStampedModel):
    exercise = models.ForeignKey(
        Exercise, on_delete=models.PROTECT, related_name="resources"
    )
    file = models.FileField(
        upload_to=get_exercise_rsc_path, storage=OverwriteStorage(), max_length=255
    )
