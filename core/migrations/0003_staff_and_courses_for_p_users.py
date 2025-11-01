from django.db import migrations


def make_staff_and_assign_courses(apps, schema_editor):
    User = apps.get_model('core', 'User')
    Course = apps.get_model('course', 'Course')

    # Ensure courses exist
    ap, _ = Course.objects.get_or_create(name='Advanced Programming', defaults={'professor_name': 'Professor'})
    cs, _ = Course.objects.get_or_create(name='Computer Simulation', defaults={'professor_name': 'Professor'})

    for i in range(1, 26):
        username = f"P{i}"
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            continue
        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=['is_staff'])
        # Assign both courses
        user.courses.add(ap)
        user.courses.add(cs)


def unassign_courses_and_unstaff(apps, schema_editor):
    User = apps.get_model('core', 'User')
    Course = apps.get_model('course', 'Course')

    try:
        ap = Course.objects.get(name='Advanced Programming')
    except Course.DoesNotExist:
        ap = None
    try:
        cs = Course.objects.get(name='Computer Simulation')
    except Course.DoesNotExist:
        cs = None

    for i in range(1, 26):
        username = f"P{i}"
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            continue
        if ap:
            user.courses.remove(ap)
        if cs:
            user.courses.remove(cs)
        if user.is_staff:
            user.is_staff = False
            user.save(update_fields=['is_staff'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_p_users'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_staff_and_assign_courses, reverse_code=unassign_courses_and_unstaff),
    ]


