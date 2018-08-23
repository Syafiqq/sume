import logging
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import authenticate, login as do_login, logout, logout
from django.http import HttpResponse
from filetransfers.api import serve_file
from django.contrib.auth.decorators import login_required

from app.app.forms import auth
from app.app.utils.arrayutil import array_except
from .models import Dokumen
from .forms import LoginForm

logger = logging.getLogger('debug')


# from filetransfers.api import serve_file


@login_required()
def index(request):
    context = {}
    return render(request, 'app/index.html', context)


def login(request):
    logout(request)
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
  
def dologin(request):
    logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                data = {
                    'username': user.username,
                }
                return redirect('/')
            else:
                return render(request, 'app/login.html', {'form': form})
                # Return an 'invalid login' error message.
                # Return an 'invalid login' error message.
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

@login_required()
def kelas(request):
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/kelas.html', context)

@login_required()
def user(request):
    context = {}
    return render(request, 'app/user.html', context)

@login_required()
def admin(request):
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/admin.html', context)

@login_required()
def detail(request, question_id):
    # dokumen = get_object_or_404(Dokumen, pk=question_id)
    # return serve_file(request, dokumen.filenya)
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/detail.html', context)



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
