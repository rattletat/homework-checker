from django.contrib import admin

from .models import Exercise, Submission


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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    fields = ["exercise", "user", "file_hash", "score", "output"]
    readonly_fields = ["exercise", "user", "file_hash", "score", "output"]
    list_display = ["created", "user", "exercise", "score"]
