from django.db import models
from user.models import User
from assignment.models import Assignment
from user.models import Course

class BrainStorm(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('user.Course', on_delete=models.CASCADE)
    assignment = models.ForeignKey('assignment.Assignment', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    # List of ideas will be accessed through the related name 'ideas'

    def __str__(self):
        return f"Brainstorm for {self.assignment.title} in {self.course.name}"