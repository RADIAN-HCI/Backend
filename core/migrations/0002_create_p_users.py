from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_p_users(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for i in range(1, 26):
        username = f"P{i}"
        if not User.objects.filter(username=username).exists():
            User.objects.create(
                username=username,
                password=make_password('1234'),
                role='TA',
            )


def delete_p_users(apps, schema_editor):
    User = apps.get_model('core', 'User')
    usernames = [f"P{i}" for i in range(1, 26)]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_p_users, reverse_code=delete_p_users),
    ]


