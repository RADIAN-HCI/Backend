from django.db import models
from brainstorming.models import BrainStorm
from django.core.validators import MinValueValidator, MaxValueValidator

class Idea(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    details = models.TextField()
    difficulty = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    innovation = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    brainstorm = models.ForeignKey(BrainStorm, on_delete=models.CASCADE, related_name='ideas')
    owner = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
