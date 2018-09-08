from app.app.utils.sess_util import LAST_URL_PATH


class RecordUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        recorded = request.build_absolute_uri()
        response = self.get_response(request)
        request.session[LAST_URL_PATH] = recorded
        # Code to be executed for each request/response after
        # the view is called.

        return response
