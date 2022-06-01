import csv

from apps.teaching.models import Lecture
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import reverse
from django.urls import path
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from sendfile import sendfile

from .models import Exercise, ExerciseResource, Submission


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

        lessons = set(exercise.lesson for exercise in model_admin.model.objects.all())
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
    fields = [
        "exercise",
        "user",
        "created",
        "submission_link",
        "score",
        "output",
    ]
    readonly_fields = [
        "exercise",
        "user",
        "created",
        "submission_link",
        "score",
        "output",
    ]
    actions = ["export_csv"]
    list_display = ["created", "exercise", "user", "score"]
    ordering = ["-created"]
    search_fields = [
        "user__name",
        "user__email",
        "user__identifier",
        "exercise__title",
        "exercise__lesson__title",
    ]
    list_filter = [LectureSubmissionFilter]

    def submission_link(self, submission):
        if submission.file:
            download_url = reverse(
                "api:submission_download", args=[submission.exercise.id, submission.id]
            )
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return "Keine Datei hochgeladen!"

    @method_decorator(staff_member_required)
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            self.model._meta
        )
        writer = csv.writer(response)

        writer.writerow(self.list_display)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in self.list_display])

        return response

    export_csv.short_description = "Export selected as CSV"
