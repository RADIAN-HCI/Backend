from django.contrib import admin
from .models import User
from .models import Course
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in User._meta.get_fields()]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Course._meta.get_fields()]
