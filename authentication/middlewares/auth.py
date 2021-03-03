from django.shortcuts import redirect


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request, *args, **kwargs):
        return_url = request.META['PATH_INFO']
        if not request.session.get('user'):
            return redirect(f'/accounts/login?return_url={return_url}')

        response = get_response(request, *args, **kwargs)
        return response

    return middleware


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.session.get('user'):
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper
