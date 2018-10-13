import datetime

from django.db import connection

from app.models import Kelas

classes = [
    Kelas(namakelas='Universitas Brawijaya', keterangan='Universitas Brawijaya', start=datetime.date(2012, 10, 2),
          end=datetime.date(2020, 10, 2)),
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_kelas RESTART IDENTITY CASCADE')


def seed():
    for cls in classes:
        cls.save()
