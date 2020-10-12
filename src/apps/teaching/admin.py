from django.contrib import admin

from .models import Lecture, Lesson

admin.site.register(Lecture)
admin.site.register(Lesson)


class LectureAdmin(admin.ModelAdmin):
    fields = "title"


class LessonAdmin(admin.ModelAdmin):
    fields = ("lecture", "title")
    readonly_fields = "lecture"
    list_display = ("lecture", "title")
