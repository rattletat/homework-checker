from apps.homework.storage import OverwriteStorage

from django.utils.timezone import now

from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel, UUIDModel

from .helpers import get_lecture_rsc_path, get_lesson_rsc_path


class GradingScale(UUIDModel):
    """Amount of points needed to reach a certain grade.
    Everything below the 4.0 threshold is rated as 5.0"""

    grade_1_0 = models.PositiveIntegerField("Punkte nötig für 1.0")
    grade_1_3 = models.PositiveIntegerField("Punkte nötig für 1.3")
    grade_1_7 = models.PositiveIntegerField("Punkte nötig für 1.7")
    grade_2_0 = models.PositiveIntegerField("Punkte nötig für 2.0")
    grade_2_3 = models.PositiveIntegerField("Punkte nötig für 2.3")
    grade_2_7 = models.PositiveIntegerField("Punkte nötig für 2.7")
    grade_3_0 = models.PositiveIntegerField("Punkte nötig für 3.0")
    grade_3_3 = models.PositiveIntegerField("Punkte nötig für 3.3")
    grade_3_7 = models.PositiveIntegerField("Punkte nötig für 3.7")
    grade_4_0 = models.PositiveIntegerField("Punkte nötig für 4.0")
    grade_5_0 = models.PositiveIntegerField("Punkte nötig für 5.0", default=0)

    def get_grade(self, score):
        if score >= self.grade_1_0:
            return "1.0"
        elif score >= self.grade_1_3:
            return "1.3"
        elif score >= self.grade_1_7:
            return "1.7"
        elif score >= self.grade_2_0:
            return "2.0"
        elif score >= self.grade_2_3:
            return "2.3"
        elif score >= self.grade_2_7:
            return "2.7"
        elif score >= self.grade_3_0:
            return "3.0"
        elif score >= self.grade_3_3:
            return "3.3"
        elif score >= self.grade_3_7:
            return "3.7"
        elif score >= self.grade_4_0:
            return "4.0"
        else:
            return "5.0"

    def __str__(self):
        return "Skala: " + "-".join(
            map(
                str,
                [
                    self.grade_1_0,
                    self.grade_1_3,
                    self.grade_1_7,
                    self.grade_2_0,
                    self.grade_2_3,
                    self.grade_2_7,
                    self.grade_3_0,
                    self.grade_3_3,
                    self.grade_3_7,
                    self.grade_4_0,
                    self.grade_5_0,
                ],
            )
        )

    class Meta:
        verbose_name = _("Benotungsskala")
        verbose_name_plural = _("Benotungsskalen")


class Lecture(UUIDModel, TimeFramedModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enrolled_lectures",
        verbose_name=_("Teilnehmer"),
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Titel"),
    )
    description = models.TextField(blank=True, verbose_name=_("Beschreibung"))
    slug = AutoSlugField(max_length=255, populate_from="title", unique=True)
    grading_scale = models.ForeignKey(
        GradingScale, on_delete=models.SET_NULL, null=True
    )

    @property
    def status(self):
        if self.start and now() < self.start:
            return "WAITING"
        if self.end and self.end < now():
            return "FINISHED"
        return "ACTIVE"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.start and self.end and self.end < self.start:
            raise ValidationError(
                _("Der Startzeitpunkt muss vor der Deadline liegen!"),
                code="invalid_date",
            )

    def get_score(self, user):
        """ Returns score of a particular user. """
        score = (
            user.submission_set
            .filter(exercise__lesson__lecture=self, score__isnull=False, exercise__rated=True)
            .values("exercise")
            .annotate(max_exercise_score=models.Max("score"))
            .aggregate(total_score=models.Sum("max_exercise_score"))["total_score"]
        )
        return score if score else 0

    class Meta:
        verbose_name = _("Vorlesung")
        verbose_name_plural = _("Vorlesungen")
        ordering = ["title"]


class Lesson(UUIDModel, TimeFramedModel):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Vorlesung"),
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel"),
    )
    description = models.TextField(blank=True, verbose_name=_("Beschreibung"))
    slug = AutoSlugField(max_length=255, populate_from="title")

    def __str__(self):
        return f"{self.lecture}: {self.title}"

    @property
    def status(self):
        if self.start and now() < self.start:
            return "WAITING"
        if self.end and self.end < now():
            return "FINISHED"
        return "ACTIVE"

    def clean(self):
        super().clean()

        if self.start and self.end and self.end < self.start:
            raise ValidationError(
                _("Der Startzeitpunkt muss vor der Deadline liegen!"),
                code="invalid_date",
            )

        if self.lecture.start and (
            (self.start and self.start < self.lecture.start)
            or (self.end and self.end < self.lecture.start)
        ):
            raise ValidationError(
                _(
                    "Die Zeitperiode der Lektion darf nicht vor Vorlesungsbeginn liegen!"
                ),
                code="invalid_date",
            )

        if self.lecture.end and (
            (self.start and self.lecture.end < self.start)
            or (self.end and self.lecture.end < self.end)
        ):
            raise ValidationError(
                _("Die Zeitperiode der Lektion darf nicht nach Vorlesungsende liegen!"),
                code="invalid_date",
            )

    class Meta:
        verbose_name = _("Lektion")

        verbose_name_plural = _("Lektionen")
        unique_together = ("lecture", "title")


class LectureResource(UUIDModel, TimeStampedModel):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel"),
    )
    file = models.FileField(
        upload_to=get_lecture_rsc_path, storage=OverwriteStorage(), max_length=255
    )

    class Meta:
        verbose_name = _("Vorlesungsmaterial")
        verbose_name_plural = _("Vorlesungmaterialien")
        unique_together = ("lecture", "title")


class LessonResource(UUIDModel, TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel"),
    )
    file = models.FileField(
        upload_to=get_lesson_rsc_path, storage=OverwriteStorage(), max_length=255
    )

    class Meta:
        verbose_name = _("Lektionsmaterial")
        verbose_name_plural = _("Lektionsmaterialen")
        unique_together = ("lesson", "title")
