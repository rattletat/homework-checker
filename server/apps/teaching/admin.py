import csv

from django.conf.locale.en import formats as en_formats
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import reverse
from django.urls import path, resolve
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.http import urlencode
from sendfile import sendfile

from .models import (
    GradingScale,
    Lecture,
    LectureResource,
    Lesson,
    LessonResource,
    RegistrationCode,
)

en_formats.DATETIME_FORMAT = "d. M Y  - H:i"


class EnrolledStudentInline(admin.TabularInline):
    model = get_user_model().enrolled_lectures.through
    fields = ["get_name", "get_identifer", "get_score", "get_grade"]
    readonly_fields = ["get_name", "get_identifer", "get_score", "get_grade"]
    extra = 0
    can_delete = False
    verbose_name = "Participant"
    verbose_name_plural = "Participants"
    ordering = ["customuser"]

    def get_formset(self, request, obj=None, **kwargs):
        self.lecture = obj
        return super(EnrolledStudentInline, self).get_formset(request, obj, **kwargs)

    def get_name(self, instance):
        return instance.customuser.name

    get_name.short_description = "Name"

    def get_identifer(self, instance):
        if identifier := instance.customuser.identifier:
            return identifier
        return ""

    get_identifer.short_description = "Student ID"

    def get_score(self, instance):
        self.score = self.lecture.get_score(instance.customuser)
        return self.score

    get_score.short_description = "Points"

    def get_grade(self, instance):
        if self.lecture.grading_scale:
            return self.lecture.grading_scale.get_grade(self.score)

    get_grade.short_description = "Grade"

    def has_add_permission(self, request, obj=None):
        return False


class LectureResourceInline(admin.TabularInline):
    model = LectureResource
    fields = ["title", "file", "resource_link"]
    readonly_fields = ["resource_link"]
    extra = 0

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
    extra = 0

    def resource_link(self, obj):
        if obj.file:
            download_view = "admin:lesson_resource_download"
            download_url = reverse(download_view, args=[obj.pk])
            return format_html('<a href="{}">Download</a>', download_url)
        else:
            return ""


class RegistrationCodeInline(admin.TabularInline):
    model = RegistrationCode
    extra = 0


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["title", "start", "end", "view_students_link"]
    fields = ["title", "description", "start", "end", "grading_scale", "download_grades_link"]
    readonly_fields = ["download_grades_link"]
    inlines = [RegistrationCodeInline, LectureResourceInline, EnrolledStudentInline]

    def view_students_link(self, obj):
        count = obj.participants.count()
        url = (
            reverse("admin:accounts_customuser_changelist")
            + "?"
            + urlencode({"enrolled_lectures__id": str(obj.id)})
        )
        return format_html('<a href="{}">{} participants</a>', url, count)

    view_students_link.short_description = "Participants"

    def get_urls(self):
        urls = super(LectureAdmin, self).get_urls()
        urls += [
            path(
                "download_resource/<slug:resource_uuid>",
                self.download_resource,
                name="lecture_resource_download",
            ),
            path(
                "download_grades/<slug:lecture_uuid>",
                self.download_grades,
                name="lecture_grades_download",
            ),
        ]
        return urls

    @method_decorator(staff_member_required)
    def download_resource(self, request, resource_uuid):
        resource = LectureResource.objects.get(id=resource_uuid)
        return sendfile(request, resource.file.path, attachment=True)

    def download_grades_link(self, lecture):
        download_view = "admin:lecture_grades_download"
        download_url = reverse(download_view, args=[lecture.pk])
        return format_html('<a href="{}">Download</a>', download_url)

    @method_decorator(staff_member_required)
    def download_grades(self, request, lecture_uuid):
        lecture = Lecture.objects.get(id=lecture_uuid)
        participants = (
            get_user_model().objects.filter(enrolled_lectures=lecture).order_by("identifier")
        )
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="results_{lecture.slug}.csv"'

        writer = csv.writer(response)
        if lecture.grading_scale:
            writer.writerow(["Identifier", "Name", "Score", "Grade"])
        else:
            writer.writerow(["Identifier", "Name", "Score"])
        for participant in participants:
            score = lecture.get_score(participant)
            if lecture.grading_scale:
                grade = lecture.grading_scale.get_grade(score)
                writer.writerow([participant.identifier, participant.name, score, grade])
            else:
                writer.writerow([participant.identifier, participant.name, score])
        return response


    download_grades_link.short_description = "Download participants results"

    class Media:
        css = {"all": ("admin/css/hide_admin_original.css",)}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = ["lecture", "title", "description", "start", "end"]
    list_filter = ["lecture"]
    list_display = ["title", "lecture"]
    inlines = [LessonResourceInline]
    ordering = ["lecture", "title"]

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["lecture"]
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
        resource = LessonResource.objects.get(id=uuid)
        return sendfile(request, resource.file.path, attachment=True)


admin.site.register(GradingScale)
