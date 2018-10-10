import datetime

from django.db import connection

from app.models import Dokumen

documents = [
    Dokumen(id=1, nama_file='Document1', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document1.pdf'),
    Dokumen(id=2, nama_file='Document2', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document2.pdf'),
    Dokumen(id=3, nama_file='Document3', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document3.pdf'),
    Dokumen(id=4, nama_file='Document4', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document4.pdf'),
    Dokumen(id=5, nama_file='Document5', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document5.pdf'),
    Dokumen(id=6, nama_file='Document6', user_id=1, pub_date=datetime.date(2018, 10, 2),
            filenya='dokumen/2018/10/02/Document6.pdf'),
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_dokumen RESTART IDENTITY CASCADE')


def seed():
    for document in documents:
        document.save()
