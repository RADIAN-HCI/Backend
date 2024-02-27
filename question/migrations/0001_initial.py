# Generated by Django 4.2.4 on 2024-02-27 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('details_original', models.TextField()),
                ('details_modified', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='question_attachments/')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='assignment.assignment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
