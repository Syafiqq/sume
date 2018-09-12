# Create your views here.
from django.shortcuts import render

from app.app.utils.arrayutil import array_merge
from app.app.utils.commonutil import initialize_form_context, fetch_message
from app.app.utils.custom.decorators import login_required


@login_required(login_url='/login')
def index(request):
    context = array_merge(initialize_form_context(), fetch_message(request))

    if request.method == 'POST':
        pass
    else:
        return render(request, '_root.html', context)
