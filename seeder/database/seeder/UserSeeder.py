import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import connection

logger = logging.getLogger('debug')


def seed():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.auth_user RESTART IDENTITY CASCADE')

    if not User.objects.filter(email='root@mail.com').exists():
        root = Group.objects.filter(name='root').first()
        ids = User.objects.create(
            username='root',
            email='root@mail.com',
            password=make_password('secret'),
            is_superuser=False,
        )
        for group in Group.objects.all():
            ids.groups.add(group)
    if not User.objects.filter(email='student@mail.com').exists():
        student = Group.objects.filter(name='student').first()
        ids = User.objects.create(
            username='student',
            email='student@mail.com',
            password=make_password('secret'),
            is_superuser=False,
        )
        ids.groups.add(student)
    if not User.objects.filter(email='organization@mail.com').exists():
        organization = Group.objects.filter(name='organization').first()
        ids = User.objects.create(
            username='organization',
            email='organization@mail.com',
            password=make_password('secret'),
            is_superuser=False,
        )
        ids.groups.add(organization)
