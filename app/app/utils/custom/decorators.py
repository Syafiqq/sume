import codecs
import pickle
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.shortcuts import resolve_url, redirect


def login_required(fnc=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if fnc:
        return actual_decorator(fnc)
    return actual_decorator


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            callback = pickle.dumps(
                {'message': {'notification': [{'msg': 'You must Login to gain access', 'level': 'info'}]}})
            messages.add_message(request, messages.INFO, codecs.encode(callback, "base64").decode(), 'callback')
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def auth_unneeded(fnc=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = auth_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if fnc:
        return actual_decorator(fnc)
    return actual_decorator


def auth_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                return view_func(request, *args, **kwargs)

            from app.app.utils.sess_util import GROUP_ID, LAST_URL_PATH
            group_id = request.session.get(GROUP_ID, 0)
            group: Group = Group.objects.filter(id=group_id).first()
            group_url_callback = '/' if group is None else ('/' + group.name)
            group_url_callback = group_url_callback if group_url_callback != request.get_full_path() else '/'
            last_url = request.session.get(LAST_URL_PATH, group_url_callback)
            last_url = group_url_callback if last_url != group_url_callback and (
                    last_url.split('/')[0] == '' or last_url.split('/') == group.name) else last_url
            callback = pickle.dumps(
                {'message': {'notification': [{'msg': 'You already authenticated', 'level': 'info'}]}})
            messages.add_message(request, messages.INFO, codecs.encode(callback, "base64").decode(), 'callback')
            return redirect(last_url)

        return _wrapped_view

    return decorator
