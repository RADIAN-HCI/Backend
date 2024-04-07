from django.db import models
from django.contrib.auth.models import AbstractUser
from course.models import Course


class User(AbstractUser):

    ROLE_CHOICES = (
        ("TA", "Teaching Assistant"),
        ("HeadTA", "Head Teaching Assistant"),
        ("Professor", "Professor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    courses = models.ManyToManyField("course.Course", related_name="users")

    def __str__(self):
        return self.username
