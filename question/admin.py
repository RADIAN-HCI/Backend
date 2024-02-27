from django.contrib import admin
from .models import Question
 
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_data = ["id"]
#   list_display = [field.name for field in Question._meta.get_fields()]
