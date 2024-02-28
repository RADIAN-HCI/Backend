from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('TA', 'Teaching Assistant'),
        ('HeadTA', 'Head Teaching Assistant'),
        ('Professor', 'Professor'),
    )
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    courses = models.ManyToManyField('Course', related_name='users')

    def __str__(self):
        return self.username

class Course(models.Model):
    name = models.CharField(max_length=100)
    professor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name