from django.contrib.auth.models import User
from django.db import connection

from app.models import Kelas

class_members = [
    {'class_id': 1, 'user_id': 1},
    {'class_id': 1, 'user_id': 2},
    {'class_id': 1, 'user_id': 3},
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_kelas_members RESTART IDENTITY CASCADE')


def seed():
    for class_member in class_members:
        user = Kelas.objects.filter(id=class_member['class_id']).first()
        user.members.add(User.objects.filter(id=class_member['user_id']).first())
