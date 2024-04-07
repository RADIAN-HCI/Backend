# Generated by Django 5.0.4 on 2024-04-07 16:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("brainstorming", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Idea",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=255)),
                ("details", models.TextField()),
                (
                    "difficulty",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "innovation",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "brainstorm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ideas",
                        to="brainstorming.brainstorm",
                    ),
                ),
            ],
        ),
    ]
