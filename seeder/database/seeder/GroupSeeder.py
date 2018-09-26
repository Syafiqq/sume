from django.contrib.auth.models import Group
from django.db import connection

groups = ['Student', 'Organization']


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.auth_group RESTART IDENTITY CASCADE')


def seed():
    for group in groups:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)
