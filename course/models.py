from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    professor_name = models.CharField(max_length=100)
    owner = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
