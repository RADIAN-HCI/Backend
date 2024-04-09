# Generated by Django 5.0.4 on 2024-04-09 01:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("question", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="lang",
            field=models.CharField(
                choices=[("fa", "Persian"), ("en", "English")],
                default="English",
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
