from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware para redirecionar usuários não autenticados para a tela de login.
    Exceção para URLs de login e registro.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(reverse('login')) and not request.path.startswith(reverse('register')):
            return redirect('login')
        response = self.get_response(request)
        return response
