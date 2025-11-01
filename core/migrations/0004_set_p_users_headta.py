from django.db import migrations


def set_head_ta(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for i in range(1, 26):
        try:
            user = User.objects.get(username=f"P{i}")
        except User.DoesNotExist:
            continue
        if user.role != 'HeadTA':
            user.role = 'HeadTA'
            user.save(update_fields=['role'])


def revert_to_ta(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for i in range(1, 26):
        try:
            user = User.objects.get(username=f"P{i}")
        except User.DoesNotExist:
            continue
        if user.role != 'TA':
            user.role = 'TA'
            user.save(update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_staff_and_courses_for_p_users'),
    ]

    operations = [
        migrations.RunPython(set_head_ta, reverse_code=revert_to_ta),
    ]


