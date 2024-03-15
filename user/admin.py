from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Course, UserProfile  # Import your custom user model

# Register your custom user model with the admin site
# admin.site.register(UserProfile, UserAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "user"
    

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Course._meta.get_fields()]
