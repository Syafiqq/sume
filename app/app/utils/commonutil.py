import codecs
import pickle

from django.contrib.messages import get_messages

from app.app.utils.arrayutil import array_merge


def fetch_message(request, custom_callback=None, custom_context=None):
    storage = get_messages(request)
    for message in storage:
        if message.extra_tags == 'callback':
            callback = pickle.loads(codecs.decode(message.message.encode(), "base64"))
            if custom_callback is not None:
                callback = custom_callback(callback)
            context = {
                'callback': callback
            }
            if custom_context is not None:
                context = array_merge(context, custom_context(callback))
            return context
