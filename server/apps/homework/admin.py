from django.contrib import admin
from django.shortcuts import reverse
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from sendfile import sendfile

from .models import Exercise, ExerciseResource, Submission


class ExerciseResourceInline(admin.TabularInline):
    model = ExerciseResource
    fields = ["title", "file", "resource_link", "loaded"]
    readonly_fields = ["resource_link"]
    extra = 1

    def resource_link(self, obj):
        if obj.file:
            download_view = "admin:exercise_resource_download"
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
                name="exercise_resource_download",
            ),
        ]
        return urls

    @method_decorator(staff_member_required)
    def download_resource(self, request, uuid):
        resource = ExerciseResource.objects.get(id=uuid)
        return sendfile(request, resource.file.path, attachment=True)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    fields = ["exercise", "user", "file_hash", "score", "output"]
    readonly_fields = ["exercise", "user", "file_hash", "score", "output"]
    list_display = ["created", "user", "exercise", "score"]
