import datetime

from django.contrib.auth.models import User
from django.db import connection

from app.models import Kelas, Dokumen

seeds = [
    {
        'class': Kelas(namakelas='Universitas Brawijaya', keterangan='Universitas Brawijaya',
                       start=datetime.date(2012, 10, 2), end=datetime.date(2020, 10, 2)),
        'members': [
            'root@mail.com',
            'student@mail.com'
        ],
        'dokumen': [
            'Dokumen1',
            'Dokumen2',
            'Dokumen3',
            'Dokumen4',
            'Dokumen5',
            'Dokumen6',
        ]
    }
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_kelas_dokumen RESTART IDENTITY CASCADE')
        cursor.execute('TRUNCATE TABLE public.app_kelas_members RESTART IDENTITY CASCADE')
        cursor.execute('TRUNCATE TABLE public.app_kelas RESTART IDENTITY CASCADE')


def seed():
    for seed in seeds:
        seed['class'].save()
        for member in seed['members']:
            seed['class'].members.add(User.objects.filter(email=member).first())
        for dokumen in seed['dokumen']:
            seed['class'].dokumen.add(Dokumen.objects.filter(nama_file=dokumen).first())
