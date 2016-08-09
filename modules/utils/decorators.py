
from django.http import HttpResponse
from django.template.response import TemplateResponse

try:
    from functools import wraps, update_wrapper
except ImportError:
    from django.utils.functional import wraps, update_wrapper

import re


def with_template(arg):
    """
    A view decorator that handles rendering.
    If the view returns a HttpResponse, it is passed intact; otherwise
    the returned value is passed as dictionary to render_to_response.
    Usage samples:
    @with_template
    def view_func(request, ...):
        return ...
    @with_template('custom/template/name.html')
    def other_view_func(request, ...):
        return ...
    """

    class TheWrapper(object):
        def __init__(self, default_template_name):
            self.default_template_name = default_template_name

        def __call__(self, func):
            def decorated_func(request, *args, **kwargs):
                ret = func(request, *args, **kwargs)
                if isinstance(ret, HttpResponse):
                    return ret
                return TemplateResponse(request, ret.get(
                    'template_name', self.default_template_name), ret)

            update_wrapper(decorated_func, func)
            return decorated_func

    if not callable(arg):
        return TheWrapper(arg)
    else:
        app_name = re.search('([^.]+)[.]views', arg.__module__).group(1)
        default_template_name = ''.join([app_name, '/', arg.__name__, '.html'])
        return TheWrapper(default_template_name)(arg)

