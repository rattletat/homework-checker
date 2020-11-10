from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.teaching.models import Lecture
from .models import CustomUser


class LectureInline(admin.TabularInline):
    model = Lecture.participants.through
    extra = 1
    max_num = 0
    readonly_fields = ["lecture"]
    can_delete = False
    verbose_name_plural = "Angemeldete Vorlesungen"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "full_name",
        "identifier",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        ("Profildaten", {"fields": ("full_name", "identifier")}),
        ("Accountdaten", {"fields": ("email", "password")}),
        ("Berechtigungen", {"fields": ("is_staff", "is_active")}),
    )
    inlines = [LectureInline]
    readonly_fields = ("full_name", "identifier", "email")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email", "full_name", "identifier")
    ordering = ("full_name",)


admin.site.register(CustomUser, CustomUserAdmin)
