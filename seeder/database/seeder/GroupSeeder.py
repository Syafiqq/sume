from django.contrib.auth.models import Group


def seed():
    for group in ['root', 'student', 'organization']:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)
