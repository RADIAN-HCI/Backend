from django.contrib import admin
from .models import BrainStorm
 
@admin.register(BrainStorm)
class BrainStormAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in BrainStorm._meta.get_fields()]
