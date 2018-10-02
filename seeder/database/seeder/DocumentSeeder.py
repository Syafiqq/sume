import datetime

from django.contrib.auth.models import User
from django.db import connection

from app.models import Dokumen

seeds = {
    'root@mail.com': [
        Dokumen(nama_file='Dokumen1', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen1.pdf'),
        Dokumen(nama_file='Dokumen2', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen2.pdf'),
        Dokumen(nama_file='Dokumen3', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen3.pdf'),
        Dokumen(nama_file='Dokumen4', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen4.pdf'),
        Dokumen(nama_file='Dokumen5', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen5.pdf'),
        Dokumen(nama_file='Dokumen6', pub_date=datetime.date(2018, 10, 2), filenya='dokumen/2018/10/02/Dokumen6.pdf'),
    ]
}


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_dokumen RESTART IDENTITY CASCADE')


def seed():
    for k, seed in seeds.items():
        user = User.objects.filter(email=k).first()
        for doc in seed:
            doc.user = user
            ids = doc.save()
