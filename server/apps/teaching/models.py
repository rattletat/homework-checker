from apps.homework.storage import OverwriteStorage
from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel, UUIDModel

from .helpers import get_lecture_rsc_path, get_lesson_rsc_path


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

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.start and self.end and self.end < self.start:
            raise ValidationError(
                _("Der Startzeitpunkt muss vor der Deadline liegen!"),
                code="invalid_date",
            )

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
        return self.title

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
                        _(
                            "Die Zeitperiode der Lektion darf nicht nach Vorlesungsende liegen!"
                        ),
                        code="invalid_date",
                    )

                    class Meta:
                        verbose_name = _("Lektion")

        verbose_name_plural = _("Lektionen")
        unique_together = ("lecture", "title")
        ordering = ["title"]


class LectureResource(UUIDModel, TimeStampedModel):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.PROTECT, related_name="resources"
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel"),
    )
    file = models.FileField(
        upload_to=get_lecture_rsc_path, storage=OverwriteStorage(), max_length=255
    )
    listed = models.BooleanField(_("Listed on website"), default=False)
    public = models.BooleanField(
        _("Downloadable via link"),
        default=False,
    )

    class Meta:
        verbose_name = _("Vorlesungsmaterial")
        verbose_name_plural = _("Vorlesungmaterialien")
        unique_together = ("lecture", "title")


class LessonResource(UUIDModel, TimeStampedModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, related_name="resources")
    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel"),
    )
    file = models.FileField(
        upload_to=get_lesson_rsc_path, storage=OverwriteStorage(), max_length=255
    )
    listed = models.BooleanField(_("Listed on website"), default=False)
    public = models.BooleanField(
        _("Downloadable via link"),
        default=False,
    )

    class Meta:
        verbose_name = _("Lektionsmaterial")
        verbose_name_plural = _("Lektionsmaterialen")
        unique_together = ("lesson", "title")
