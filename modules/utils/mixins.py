from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BreadcrumbsMixin(object):
    """ Mixin that pass breadcrumbs to request """
    breadcrumbs = {}

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs = self.breadcrumbs
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    """ Mixin class, that decorates dispatch to force login """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """ dispatch """
        return super().dispatch(request, *args, **kwargs)
