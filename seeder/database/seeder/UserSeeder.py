import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import connection

users = [
    User(id=1, username='root', email='root@mail.com', password=make_password('secret'), is_superuser=False),
    User(id=2, username='student', email='student@mail.com', password=make_password('secret'), is_superuser=False),
    User(id=3, username='organization', email='organization@mail.com', password=make_password('secret'), is_superuser=False)
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.auth_user RESTART IDENTITY CASCADE')


def seed():
    for user in users:
        if not User.objects.filter(id=user.id).exists():
            user.save()
