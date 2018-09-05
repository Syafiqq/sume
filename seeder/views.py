# Create your views here.
import datetime

from django.http import HttpResponse

from seeder.database.seeder import UserSeeder


def index(request):
    UserSeeder.seed()

    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
