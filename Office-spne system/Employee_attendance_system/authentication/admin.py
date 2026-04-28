from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # List view (table)
    list_display = (
        "user",
        "employee_id",
        "phone",
        "department",
        "designation",
        "city",
        "country"
    )

    # Search bar
    search_fields = (
        "user__username",
        "employee_id",
        "phone",
        "department",
        "designation"
    )

    # Filters (right side)
    list_filter = (
        "department",
        "designation",
        "gender",
        "marital_status",
        "country"
    )

    # Readonly fields
    readonly_fields = ("employee_id",)

    # Field grouping (VERY IMPORTANT 🔥)
    fieldsets = (

        ("User Info", {
            "fields": ("user", "employee_id", "profile_image")
        }),

        ("Personal Info", {
            "fields": (
                "phone", "alternate_phone", "address",
                "city", "state", "country", "pincode",
                "dob", "gender", "marital_status",
                "blood_group", "nationality"
            )
        }),

        ("Job Info", {
            "fields": (
                "department", "designation", "joining_date",
                "shift", "salary", "manager_name", "work_location"
            )
        }),

        ("Education", {
            "fields": (
                "qualification", "college_name", "passing_year"
            )
        }),

        ("Documents", {
            "fields": (
                "aadhaar_number", "pan_number"
            )
        }),

        ("Emergency Contact", {
            "fields": (
                "emergency_contact_name",
                "emergency_contact_phone",
                "emergency_relation"
            )
        }),

        ("Social Links", {
            "fields": (
                "linkedin", "instagram"
            )
        }),

        ("Other Info", {
            "fields": (
                "bio", "skills", "hobbies"
            )
        }),
    )