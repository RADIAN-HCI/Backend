from django.db import models
from core.models import User
from assignment.models import Assignment
from core.models import Course


class BrainStorm(models.Model):
    LANG_CHOICES = (("fa", "Persian"), ("en", "English"))

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    assignment = models.ForeignKey("assignment.Assignment", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    lang = models.CharField(max_length=20, choices=LANG_CHOICES)
    # List of ideas will be accessed through the related name 'ideas'

    def __str__(self):
        return f"Brainstorm for {self.assignment.title} in {self.course.name}"
