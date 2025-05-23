from django.http import HttpResponseForbidden
from functools import wraps

def role_required(*roles):
    """
    Decorador que verifica se o usuário pertence a um ou mais grupos.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Você precisa estar autenticado para acessar esta página.")

            if not request.user.groups.filter(name__in=roles).exists():
                return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
