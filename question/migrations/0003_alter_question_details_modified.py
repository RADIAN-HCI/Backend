# Generated by Django 4.2.4 on 2024-04-24 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_question_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='details_modified',
            field=models.TextField(blank=True),
        ),
    ]
