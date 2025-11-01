from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_assignment_deadline'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedPDF',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=512)),
                ('file_size_bytes', models.BigIntegerField()),
                ('mime_type', models.CharField(default='application/pdf', max_length=64)),
                (
                    'assignment',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generated_pdfs', to='assignment.assignment'),
                ),
                (
                    'author',
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]


