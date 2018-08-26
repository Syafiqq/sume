import codecs
import pickle

from django.contrib.messages import get_messages

from app.app.utils.arrayutil import array_merge


def fetch_message(request, custom_callback=None, custom_context=None):
    context = {}
    storage = get_messages(request)
    for message in storage:
        if message.extra_tags == 'callback':
            callback = pickle.loads(codecs.decode(message.message.encode(), "base64"))
            if custom_callback is not None:
                callback = custom_callback(callback)
            context = callback
            if custom_context is not None:
                context = array_merge(context, custom_context(callback))
    return context


def initialize_form_context():
    return {
        'form': {
            'data': {},
            'errors': {}
        },
        'message': {
            'notification': {},
            'alert': {},
            'custom': {}
        },
        'data': {}
    }


def base_url(request):
    """
    @see https://gist.github.com/crackjack/8120686
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return scheme + request.get_host()
