from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel, UUIDModel

from apps.teaching.models import Lesson


class Exercise(UUIDModel):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name=_("Lektion")
    )

    title = models.CharField(max_length=100, verbose_name=_("Titel"))
    slug = AutoSlugField(populate_from="title")
    description = models.TextField(blank=True, verbose_name=_("Beschreibung"))
    max_score = models.PositiveSmallIntegerField(verbose_name=_("Maximale Punktzahl"))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exercise, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Aufgabe")
        verbose_name_plural = _("Aufgaben")
        ordering = ["title"]


class Submission(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField()
    output = models.TextField(blank=True)

    def clean(self):
        super().clean()

        lesson_start = self.exercise.lesson.start
        lesson_end = self.exercise.lesson.end
        if lesson_start and self.created < lesson_start:
            raise ValidationError(
                _("Eine Submission kann nicht vor Start der Lektion erfolgen."),
                code="invalid_submission_date",
            )
        if lesson_end and lesson_end < self.created:
            raise ValidationError(
                _("Eine Submission kann nicht vor Start der Lektion erfolgen."),
                code="invalid_submission_date",
            )
