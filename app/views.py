import codecs
import logging
import pickle

from django.contrib import messages
from django.contrib.auth import authenticate, login as do_login
# from filetransfers.api import serve_file
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from app.app.forms import auth
from app.app.utils.arrayutil import array_except, array_merge
from app.app.utils.custom.decorators import login_required
from .forms import LoginForm
from .models import Dokumen

logger = logging.getLogger('debug')


# from filetransfers.api import serve_file


@login_required(login_url='/login')
def index(request):
    context = {}
    return render(request, 'app/index.html', context)


def login(request):
    context = {}

    storage = get_messages(request)
    for message in storage:
        if message.extra_tags == 'callback':
            callback = pickle.loads(codecs.decode(message.message.encode(), "base64"))
            context = {
                'email': callback['data']['email'] if 'data' in callback and 'email' in callback['data'] else "",
                'password': callback['data']['password'] if 'data' in callback and 'password' in callback[
                    'data'] else "",
                'callback': callback
            }

    if request.method == 'POST':
        form = auth.Login(request.POST)
        context = array_merge(context, array_except(dict(form.data), 'csrfmiddlewaretoken'))
        if form.is_valid():
            user_data = authenticate(request,
                                     username=form.cleaned_data.get('email'),
                                     password=form.cleaned_data.get('password'))
            if user_data is not None:
                do_login(request, user_data)
                callback = pickle.dumps({
                    'message': {
                        'notification': [
                            {'msg': 'Login Success', 'level': 'success'}
                        ]
                    }})
                messages.add_message(request, messages.INFO, codecs.encode(callback, "base64").decode(), 'callback')
                return redirect(
                    request.POST.get('next') if (request.POST.get('next') and request.POST.get('next') != "") else '/')
            else:
                context['errors'] = {'email': 'Account does not exists.'}
                return render(request, 'app/login.html', context)
        else:
            context['errors'] = dict(form.errors)
            return render(request, 'app/login.html', context)
    else:
        if request.GET.get('next') and request.GET.get('next') != "":
            context['next'] = request.GET.get('next')
        return render(request, 'app/login.html', context)


def register(request):
    context = {}

    storage = get_messages(request)
    for message in storage:
        if message.extra_tags == 'callback':
            callback = pickle.loads(codecs.decode(message.message.encode(), "base64"))
            context = {
                'callback': callback
            }

    if request.method == 'POST':
        form = auth.Register(request.POST)
        context = array_merge(context, array_except(dict(form.data), 'csrfmiddlewaretoken'))
        if form.is_valid():
            if form.cleaned_data.get('password') != form.cleaned_data.get('password_conf'):
                context['errors'] = {'password': 'Password Unequal', 'password_conf': 'Password Unequal'}
                return render(request, 'app/register.html', context)
            elif len(User.objects.filter(email=form.cleaned_data.get('email'))) > 0:
                context['errors'] = {'email': 'Email exists'}
                return render(request, 'app/register.html', context)
            else:
                account = User(username=form.cleaned_data.get('username'),
                               email=form.cleaned_data.get('email'),
                               password=make_password(form.cleaned_data.get('password')))
                try:
                    account.save()
                except IntegrityError:
                    context['errors'] = {'username': 'Username is already taken'}
                    return render(request, 'app/register.html', context)
                callback = pickle.dumps({
                    'message': {
                        'alert': [
                            {'msg': 'Registration Success', 'level': 'success'}
                        ]
                    },
                    'data': {
                        'email': form.cleaned_data.get('email'),
                        'password': form.cleaned_data.get('password')
                    }
                })
                messages.add_message(request, messages.INFO, codecs.encode(callback, "base64").decode(), 'callback')
                return redirect('/login')
        else:
            context['errors'] = dict(form.errors)
            return render(request, 'app/register.html', context)
    else:
        return render(request, 'app/register.html', context)

  
def dologin(request):
    
    (request)
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


@login_required(login_url='/login')
def kelas(request):
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/kelas.html', context)


@login_required(login_url='/login')
def user(request):
    context = {}
    return render(request, 'app/user.html', context)


@login_required(login_url='/login')
def admin(request):
    latest_dokumen_list = Dokumen.objects.order_by('-pub_date')[:5]
    context = {
        'latest_dokumen_list': latest_dokumen_list,
    }
    return render(request, 'app/admin.html', context)


@login_required(login_url='/login')
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
