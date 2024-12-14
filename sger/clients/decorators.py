from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.db import connection


def executar_consulta(sql, parametros=None):
    """
    Função auxiliar para executar consultas SQL.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, parametros or [])
        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()


def role_required(*required_roles):
    """
    Decorador para verificar se o usuário possui um dos papéis especificados.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_id = request.session.get('user_id')

            if not user_id:
                messages.error(request, 'Você precisa estar logado para acessar esta página.')
                return redirect('login')

            # Verifica o papel do usuário
            sql_get_roles = "SELECT role FROM UserRoles WHERE user_id = %s"
            user_roles = executar_consulta(sql_get_roles, [user_id])

            # Transforma os papéis do usuário em uma lista de strings
            user_roles = [role[0] for role in user_roles]

            # Verifica se o papel do usuário está nos papéis permitidos
            if not any(role in required_roles for role in user_roles):
                messages.error(request, 'Acesso negado! Você não tem permissão para acessar esta página.')
                return redirect('home')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
