from django.db import connection

from app.models import Kelas, Dokumen

class_documents = [
    {'class_id': 1, 'dokumen_id': 1},
    {'class_id': 1, 'dokumen_id': 2},
    {'class_id': 1, 'dokumen_id': 3},
    {'class_id': 1, 'dokumen_id': 4},
    {'class_id': 1, 'dokumen_id': 5},
    {'class_id': 1, 'dokumen_id': 6},
]


def truncate():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE public.app_kelas_dokumen RESTART IDENTITY CASCADE')


def seed():
    for class_document in class_documents:
        user = Kelas.objects.filter(id=class_document['class_id']).first()
        user.dokumen.add(Dokumen.objects.filter(id=class_document['dokumen_id']).first())
