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
    list_display = ["get_lecture", "lesson", "title"]
    list_filter = ["lesson", "title"]
    fields = [
        "lesson",
        "title",
        "max_score",
        "description",
        "programming_language",
        "tests",
        "min_upload_size",
        "max_upload_size",
        "timeout",
    ]
    readonly_fields = ["lesson"]
    inlines = [ExerciseResourceInline]

    def get_lecture(self, obj):
        return obj.lesson.lecture

    get_lecture.short_description = "Vorlesung"

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["lesson"]
        else:
            return []

    def get_urls(self):
        urls = super(ExerciseAdmin, self).get_urls()
        urls += [
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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    fields = ["exercise", "user", "submission_link", "score", "output"]
    readonly_fields = ["exercise", "user", "submission_link", "score", "output"]
    list_display = ["created", "exercise", "score", "user"]

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
