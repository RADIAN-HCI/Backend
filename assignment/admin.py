from django.contrib import admin
from .models import Assignment
 
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Assignment._meta.get_fields()]
