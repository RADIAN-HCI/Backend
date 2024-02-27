from django.contrib import admin
from .models import Idea
 
@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Idea._meta.get_fields()]
