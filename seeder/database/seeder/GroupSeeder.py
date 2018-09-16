from django.contrib.auth.models import Group

groups = ['Student', 'Organization']


def seed():
    for group in groups:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)
