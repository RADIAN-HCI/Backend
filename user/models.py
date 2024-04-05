from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ("TA", "Teaching Assistant"),
        ("HeadTA", "Head Teaching Assistant"),
        ("Professor", "Professor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # courses = models.ManyToManyField("Course", related_name="users")


# class UserProfile(models.Model):
#     ROLE_CHOICES = (
#         ('TA', 'Teaching Assistant'),
#         ('HeadTA', 'Head Teaching Assistant'),
#         ('Professor', 'Professor'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     courses = models.ManyToManyField('Course', related_name='users')

#     def __str__(self):
#         return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    professor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
