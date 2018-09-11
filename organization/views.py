# Create your views here.
from django.http import HttpResponse


def index(request):
    html = "<html><body>Index of Organization</body></html>"
    return HttpResponse(html)
