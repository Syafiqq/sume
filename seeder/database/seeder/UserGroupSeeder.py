from django.contrib.auth.models import User, Group
from django.db import connection

user_groups = [
    {'user_id': 1, 'group_id': 1},
    {'user_id': 1, 'group_id': 2},
    {'user_id': 2, 'group_id': 1},
    {'user_id': 3, 'group_id': 2},
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.auth_user_groups RESTART IDENTITY CASCADE')


def seed():
    for user_group in user_groups:
        user = User.objects.filter(id=user_group['user_id']).first()
        user.groups.add(Group.objects.filter(id=user_group['group_id']).first())
