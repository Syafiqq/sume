# Create your views here.
from django.http import HttpResponse

from app.app.utils.custom.decorators import login_required


@login_required(login_url='/login')
def index(request):
    html = "<html><body>Index of Organization</body></html>"
    return HttpResponse(html)
