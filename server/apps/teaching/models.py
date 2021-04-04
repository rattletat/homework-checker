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
    """Score needed to reach a certain grade.
    Everything below the 4.0 threshold is graded as 5.0"""

    grade_1_0 = models.PositiveIntegerField("Points needed to reach 1.0")
    grade_1_3 = models.PositiveIntegerField("Points needed to reach 1.3")
    grade_1_7 = models.PositiveIntegerField("Points needed to reach 1.7")
    grade_2_0 = models.PositiveIntegerField("Points needed to reach 2.0")
    grade_2_3 = models.PositiveIntegerField("Points needed to reach 2.3")
    grade_2_7 = models.PositiveIntegerField("Points needed to reach 2.7")
    grade_3_0 = models.PositiveIntegerField("Points needed to reach 3.0")
    grade_3_3 = models.PositiveIntegerField("Points needed to reach 3.3")
    grade_3_7 = models.PositiveIntegerField("Points needed to reach 3.7")
    grade_4_0 = models.PositiveIntegerField("Points needed to reach 4.0")
    grade_5_0 = models.PositiveIntegerField("Points needed to reach 5.0", default=0)

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
        return "Scale: " + "-".join(
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


class Lecture(UUIDModel, TimeFramedModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enrolled_lectures",
    )
    title = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField(blank=True)
    slug = AutoSlugField(max_length=255, populate_from="title", unique=True, always_update=True)
    grading_scale = models.ForeignKey(
        GradingScale, on_delete=models.SET_NULL, blank=True, null=True
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
                _("Lecture end must be after lecture start!"),
                code="invalid_date",
            )

    def get_score(self, user):
        """ Returns score of a particular user. """
        score = (
            user.submission_set
            .filter(exercise__lesson__lecture=self, score__isnull=False, exercise__graded=True)
            .values("exercise")
            .annotate(max_exercise_score=models.Max("score"))
            .aggregate(total_score=models.Sum("max_exercise_score"))["total_score"]
        )
        return score if score else 0

    class Meta:
        ordering = ["title"]


class Lesson(UUIDModel, TimeFramedModel):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField(blank=True)
    slug = AutoSlugField(max_length=255, populate_from="title", always_update=True)

    def __str__(self):
        return self.title

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
                _("End of lesson must be after lesson starts!"),
                code="invalid_date",
            )

        if self.lecture.start and (
            (self.start and self.start < self.lecture.start)
            or (self.end and self.end < self.lecture.start)
        ):
            raise ValidationError(
                _(
                    "Lesson cannot start before lecture starts!"
                ),
                code="invalid_date",
            )

        if self.lecture.end and (
            (self.start and self.lecture.end < self.start)
            or (self.end and self.lecture.end < self.end)
        ):
            raise ValidationError(
                _("Lesson cannot end after lecture ends!"),
                code="invalid_date",
            )

    class Meta:
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
        verbose_name = _("Lesson Resource")
        verbose_name_plural = _("Lesson Resources")
        unique_together = ("lesson", "title")


class RegistrationCode(UUIDModel):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="registration_codes",
    )
    code = models.CharField(
        max_length=50,
        unique=True,
    )
