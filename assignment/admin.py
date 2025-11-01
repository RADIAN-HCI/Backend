from django.contrib import admin
from .models import Assignment, GeneratedPDF
 
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Assignment._meta.get_fields()]


@admin.register(GeneratedPDF)
class GeneratedPDFAdmin(admin.ModelAdmin):
  list_display = ("id", "assignment", "author", "file_name", "file_size_bytes", "created_at")
  list_filter = ("assignment", "author", "created_at")
  search_fields = ("file_name", "assignment__title", "author__username")
