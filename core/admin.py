from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Course, User  # Use the custom user model

# Register your custom user model with the admin site
# admin.site.register(UserProfile, UserAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = "user"


# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [UserProfileInline]

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)

    # Show role (and courses) on the user edit page
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role & Access", {"fields": ("role",)}),
        ("Courses", {"fields": ("courses",)}),
    )

    # Include role (and courses) on the user creation page
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role & Access", {"fields": ("role",)}),
        ("Courses", {"fields": ("courses",)}),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_data = ["id"]


#   list_display = [field.name for field in Course._meta.get_fields()]
