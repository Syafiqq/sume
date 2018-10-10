from django.contrib.auth.models import Group
from django.db import connection

groups = [
    Group(id=1, name='Student'),
    Group(id=2, name='Organization')
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.auth_group RESTART IDENTITY CASCADE')


def seed():
    for group in groups:
        if not Group.objects.filter(id=group.id).exists():
            group.save()
