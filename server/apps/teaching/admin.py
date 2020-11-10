from django.contrib import admin

from .models import Lecture, Lesson
from apps.teaching.models import LectureResource, LessonResource

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import reverse
from sendfile import sendfile


class LectureResourceInline(admin.TabularInline):
    model = LectureResource
    fields = ["title", "file", "resource_link"]
    readonly_fields = ["resource_link"]
    extra = 1

    def resource_link(self, obj):
        if obj.file:
            download_view = "admin:lecture_resource_download"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return ""


class LessonResourceInline(admin.TabularInline):
    model = LessonResource
    fields = ["title", "file", "resource_link"]
    readonly_fields = ["resource_link"]
    extra = 1

    def resource_link(self, obj):
        if obj.file:
            download_view = "admin:lesson_resource_download"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return ""


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    fields = ["title", "description", "participants", "start", "end"]
    inlines = [LectureResourceInline]

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["title", "participants"]
        else:
            return ["participants"]

    def get_urls(self):
        urls = super(LectureAdmin, self).get_urls()
        urls += [
            path(
                "download_resource/<slug:uuid>",
                self.download_resource,
                name="lecture_resource_download",
            ),
        ]
        return urls

    @method_decorator(staff_member_required)
    def download_resource(self, request, uuid):
        resource = LectureResource.objects.get(id=uuid)
        return sendfile(request, resource.file.path, attachment=True)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = ["lecture", "title", "description", "start", "end"]
    list_filter = ["lecture"]
    list_display = ["lecture", "title"]
    inlines = [LessonResourceInline]

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["lecture", "title"]
        else:
            return []

    def get_urls(self):
        urls = super(LessonAdmin, self).get_urls()
        urls += [
            path(
                "download_resource/<slug:uuid>",
                self.download_resource,
                name="lesson_resource_download",
            ),
        ]
        return urls

    @method_decorator(staff_member_required)
    def download_resource(self, request, uuid):
        resource = LectureResource.objects.get(id=uuid)
        return sendfile(request, resource.file.path, attachment=True)
