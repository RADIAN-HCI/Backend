from django.db import models

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey('assignment.Assignment', on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    details_original = models.TextField()
    details_modified = models.TextField()
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)  # Assuming you have a User model
    attachment = models.FileField(upload_to='question_attachments/', null=True, blank=True)

    def __str__(self):
        return self.title