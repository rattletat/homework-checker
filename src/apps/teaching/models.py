from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from model_utils.models import UUIDModel


class Lecture(UUIDModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lecture, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teaching:lecture_detail", args=[self.slug])


class Lesson(UUIDModel):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lecture}: {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "teaching:lesson_detail",
            kwargs={"lecture_slug": self.lecture.slug, "lesson_slug": self.slug},
        )

    class Meta:
        unique_together = ("lecture", "title")
