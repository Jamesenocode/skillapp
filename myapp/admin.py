from django.contrib import admin
from .models import TrainingApplication, AdminActivityLog

# Register the log model here since it doesn't have a decorator
admin.site.register(AdminActivityLog)

@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "surname",
        "first_name",
        "program",
        "phone_number",
        "status",
        "application_date",
    )

    list_filter = (
        "status",
        "program",
        "category",
        "duration",
    )

    search_fields = (
        "surname",
        "first_name",
        "middle_name",
        "phone_number",
        "guardian_phone_number",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "application_date",
    )

    fieldsets = (
        ("Personal Data", {
            "fields": (
                "surname",
                "first_name",
                "middle_name",
                "address",
                "age",
                "category",
                "phone_number",
                "level_of_education",
            )
        }),
        ("Training Details", {
            "fields": (
                "program",
                "duration",
                "start_date",
                "end_date",
            )
        }),
        ("Guardian Information", {
            "fields": (
                "guardian_name",
                "guardian_address",
                "guardian_phone_number",
            )
        }),
        ("Uploads", {
            "fields": (
                "student_passport",
                "guardian_passport",
            )
        }),
        ("Review", {
            "fields": (
                "status",
                "admin_message",
                "application_date",
            )
        }),
    )

    ordering = (
        "-application_date",
    )