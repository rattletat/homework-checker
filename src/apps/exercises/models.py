from django.db import models

from apps.teaching.models import Lesson
from model_utils.models import UUIDModel


class Exercise(UUIDModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lesson.lecture}: {self.lesson.title} ({self.title})"
