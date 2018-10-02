# Create your views here.
import datetime

from django.http import HttpResponse

from seeder.database.seeder import UserSeeder, GroupSeeder, DocumentSeeder, ClassSeeder


def index(request):
    UserSeeder.truncate()
    GroupSeeder.truncate()
    DocumentSeeder.truncate()
    ClassSeeder.truncate()

    GroupSeeder.seed()
    UserSeeder.seed()
    DocumentSeeder.seed()
    ClassSeeder.seed()

    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
