from django.db import models
from core.models import Course
from django.conf import settings


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
    owner = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    # 'questions' field is defined as a ManyToManyField in Assignment class

    def __str__(self):
        return self.title


class GeneratedPDF(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="generated_pdfs"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    file_size_bytes = models.BigIntegerField()
    mime_type = models.CharField(max_length=64, default="application/pdf")

    def __str__(self):
        return f"PDF #{self.id} for {self.assignment.title} ({self.file_name})"
