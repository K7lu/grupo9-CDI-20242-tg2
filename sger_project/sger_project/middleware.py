from django.utils.deprecation import MiddlewareMixin

class AddUserToContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        """
        Adiciona o nome do usuário ao contexto global do template.
        """
        if request.user.is_authenticated:
            response.context_data['logged_user'] = request.user.username
        else:
            response.context_data['logged_user'] = None
        return response
