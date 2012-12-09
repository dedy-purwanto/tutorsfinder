from functools import wraps

from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def login_and_email_required(view):

    @wraps(view)
    def inner(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated():
            return redirect(reverse("login"))

        return view(request, *args, **kwargs)
    return inner

class LoginRequiredMixin(object):

    @method_decorator(login_and_email_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
