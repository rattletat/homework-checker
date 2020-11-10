from django.contrib import admin

from .models import Exercise, Submission


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["get_lecture", "lesson", "title"]
    list_filter = ["lesson", "title"]
    fields = ["lesson", "title", "max_score", "description"]
    readonly_fields = ["lesson"]

    def get_lecture(self, obj):
        return obj.lesson.lecture

    get_lecture.short_description = "Vorlesung"


# @admin.register(Submission)
# class Submission(admin.ModelAdmin):
#     fields = ["title"]
#     list_display = ["title"]
