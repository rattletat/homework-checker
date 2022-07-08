from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.teaching.models import Lecture
from .models import CustomUser
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group


class LectureInline(admin.TabularInline):
    model = Lecture.participants.through
    extra = 1
    max_num = 0
    readonly_fields = ["lecture"]
    verbose_name_plural = "Enrolled Lectures"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "name",
        "identifier",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "enrolled_lectures",
    )
    fieldsets = (
        ("Profil data", {"fields": ("name", "identifier")}),
        ("Account data", {"fields": ("email", "password")}),
        ("Roles", {"fields": ("is_staff", "is_active")}),
    )
    inlines = [LectureInline]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "identifier", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email", "name", "identifier", "id")
    ordering = ("identifier",)

    def get_readonly_fields(self, _, obj=None):
        if obj:
            return ["name", "email"]
        else:
            return []


admin.site.register(CustomUser, CustomUserAdmin)

# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=CustomUser.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
