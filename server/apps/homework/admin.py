from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url
from django.shortcuts import reverse
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from sendfile import sendfile

from .models import Exercise, ExerciseResource, Submission
from apps.teaching.models import Lecture

from django.contrib.admin import SimpleListFilter


class ExerciseLectureFilter(SimpleListFilter):
    title = "lecture"
    parameter_name = "lecture"

    def lookups(self, request, model_admin):

        lectures = set(
            exercise.lesson.lecture for exercise in model_admin.model.objects.all()
        )
        return [(lecture.id, lecture.title) for lecture in lectures]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lesson__lecture=self.value())

class ExerciseLessonFilter(SimpleListFilter):
    title = "lesson"
    parameter_name = "lesson"

    def lookups(self, request, model_admin):

        lessons = set(
            exercise.lesson for exercise in model_admin.model.objects.all()
        )
        return [(lesson.id, lesson.title) for lesson in lessons]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lesson=self.value())


class ExerciseResourceInline(admin.TabularInline):
    model = ExerciseResource
    fields = ["file", "resource_link"]
    readonly_fields = ["resource_link"]
    extra = 1

    def resource_link(self, obj):
        if obj.file:
            download_view = "admin:homework_download_resource"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return ""


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "get_lecture"]
    list_filter = [ExerciseLectureFilter, ExerciseLessonFilter]
    fields = [
        "lesson",
        "title",
        "max_score",
        "multiplier",
        "description",
        "programming_language",
        "tests",
        "tests_link",
        "min_upload_size",
        "max_upload_size",
        "timeout",
        "graded",
    ]
    readonly_fields = ["lesson", "tests_link"]
    inlines = [ExerciseResourceInline]

    def get_lecture(self, obj):
        return obj.lesson.lecture

    get_lecture.short_description = "Lecture"

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["lesson", "tests_link"]
        else:
            return ["tests_link"]

    def tests_link(self, obj):
        if obj.tests:
            download_view = "admin:homework_download_tests"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return ""

    def get_urls(self):
        urls = super(ExerciseAdmin, self).get_urls()
        urls += [
            path(
                "download_tests/<slug:uuid>",
                self.download_tests,
                name="homework_download_tests",
            ),
            path(
                "download_resource/<slug:uuid>",
                self.download_resource,
                name="homework_download_resource",
            ),
        ]
        return urls

    @method_decorator(staff_member_required)
    def download_resource(self, request, uuid):
        resource = ExerciseResource.objects.get(id=uuid)
        return sendfile(request, resource.file.path, attachment=True)

    @method_decorator(staff_member_required)
    def download_tests(self, request, uuid):
        exercise = Exercise.objects.get(id=uuid)
        return sendfile(request, exercise.tests.path, attachment=True)


class LectureSubmissionFilter(SimpleListFilter):
    title = "lecture"
    parameter_name = "lecture"

    def lookups(self, request, model_admin):
        return [(lecture.id, lecture.title) for lecture in Lecture.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(exercise__lesson__lecture=self.value())


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    fields = ["exercise", "user", "created", "submission_link", "score", "output"]
    readonly_fields = [
        "exercise",
        "user",
        "created",
        "submission_link",
        "score",
        "output",
    ]
    list_display = ["created", "exercise", "score", "user"]
    ordering = ["-created"]
    search_fields = [
        "user__name",
        "user__email",
        "user__identifier",
        "exercise__title",
        "exercise__lesson__title",
    ]
    list_filter = [LectureSubmissionFilter]

    def get_urls(self):
        urls = super(SubmissionAdmin, self).get_urls()
        urls += [
            path(
                "download-submission/<slug:uuid>",
                self.download_submission,
                name="homework_download_submission",
            ),
        ]
        return urls

    def submission_link(self, obj):
        if obj.file:
            download_view = "admin:homework_download_submission"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return "Noch keine Datei hochgeladen!"

    @method_decorator(staff_member_required)
    def download_submission(self, request, uuid):
        submission = Submission.objects.get(id=uuid)
        return sendfile(request, submission.file.path, attachment=True)
