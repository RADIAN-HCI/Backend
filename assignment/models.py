from django.db import models
from core.models import Course


class Assignment(models.Model):
    TYPE_CHOICES = (
        ("Theoretical", "Theoretical"),
        ("Practical", "Practical"),
        ("Project", "Project"),
    )

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, related_name="assignments"
    )  # Assuming you have a Course model
    title = models.CharField(max_length=255)
    assignment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    deadline = models.DateField()  
    # 'questions' field is defined as a ManyToManyField in Assignment class

    def __str__(self):
        return self.title
