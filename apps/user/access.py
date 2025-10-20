from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def superuser_or_admin_required(view_func):
    def check_perms(user):
        if user.is_authenticated:
            return user.is_superuser or user.groups.filter(name='Admin').exists()
        return False

    def decorator(request, *args, **kwargs):
        if check_perms(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")

    return decorator