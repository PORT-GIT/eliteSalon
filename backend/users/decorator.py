from django.http import HttpResponseForbidden
from functools import wraps

def employee_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated and hasattr(request.user, 'employee_profile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access page")

    return _wrapped_view 

def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access page")

    return _wrapped_view

# with this access to the django admin panel is restricted to users with admin-profile or superusers
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated and (hasattr(request.user, 'admin_profile') or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access page")

    return _wrapped_view
