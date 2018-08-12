import logging

from django.contrib.auth import authenticate, login as do_login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from app.app.forms import auth
from app.app.utils.arrayutil import array_except
from .models import Dokumen

logger = logging.getLogger('debug')


# from filetransfers.api import serve_file


def index(request):
    context = {}
    return render(request, 'app/index.html', context)


def login(request):
    if request.method == 'POST':
        form = auth.Login(request.POST)
        data = array_except(dict(form.data), 'csrfmiddlewaretoken')
        if form.is_valid():
            user_data = authenticate(request,
                                     username=form.cleaned_data.get('email'),
                                     password=form.cleaned_data.get('password'))
            if user_data is not None:
                do_login(request, user_data)
                return render(request, 'app/login.html')
            else:
                data['errors'] = {'email': 'Account does not exists.'}
                return render(request, 'app/login.html', data)
        else:
            data['errors'] = dict(form.errors)
            return render(request, 'app/login.html', data)
    else:
        return render(request, 'app/login.html', dict(auth.Login().data))


def register(request):
    context = {}
    return render(request, 'app/register.html', context)


def user(request):
    context = {}
    return render(request, 'app/user.html', context)


def detail(request, question_id):
    dokumen = get_object_or_404(Dokumen, pk=question_id)
    return serve_file(request, dokumen.filenya)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def openfile(request, question_id):
    filename = Dokumen.filenya.name.split('/')[-1]
    response = HttpResponse(object_name.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
