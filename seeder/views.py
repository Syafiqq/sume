# Create your views here.
import datetime

from django.http import HttpResponse

from seeder.database.seeder import UserSeeder, GroupSeeder, DocumentSeeder, ClassSeeder, UserGroupSeeder, \
    ClassMemberSeeder, ClassDokumenSeeder


def index(request):
    ClassDokumenSeeder.truncate()
    ClassMemberSeeder.truncate()
    ClassSeeder.truncate()
    DocumentSeeder.truncate()
    UserGroupSeeder.truncate()
    UserSeeder.truncate()
    GroupSeeder.truncate()

    GroupSeeder.seed()
    UserSeeder.seed()
    UserGroupSeeder.seed()
    DocumentSeeder.seed()
    ClassSeeder.seed()
    ClassMemberSeeder.seed()
    ClassDokumenSeeder.seed()

    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
