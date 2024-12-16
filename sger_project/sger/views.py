from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from sger.utils.database import executar_consulta
from django.db import connection
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from datetime import datetime

from datetime import datetime

@login_required
def home_view(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)  

    context = {
        'is_master': 'Master' in user_groups,
        'is_admin': 'Administradores' in user_groups or 'Master' in user_groups,
        'is_employee': 'Funcionario' in user_groups,
        'is_client': 'Cliente' in user_groups,
    }
    return render(request, 'sger/home.html', context)

# Login
def login_view(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {username}!")
            return redirect('home')  # Redireciona para a home
        else:
            messages.error(request, "Usuário ou senha incorreto. Tente novamente.")

    return render(request, 'sger/login.html')

def logout_view(request):
    request.session.flush()  # Limpa a sessão do usuário
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, 'Logout realizado com sucesso!')
    logout(request)
    return redirect('login')


def execute_query(sql, params=None):
    """
    Função auxiliar para executar consultas SQL brutas.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()
        


def register_view(request):
    if request.method == 'POST':
        try:
            # Captura dados do formulário
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            hashed_password = make_password(password)

            # Verifica duplicidade de usuário ou email
            sql_check_username = "SELECT COUNT(*) FROM auth_user WHERE username = %s"
            sql_check_email = "SELECT COUNT(*) FROM auth_user WHERE email = %s"

            if execute_query(sql_check_username, [username])[0][0] > 0:
                messages.error(request, "O nome de usuário já existe.")
                return render(request, 'sger/register.html')

            if execute_query(sql_check_email, [email])[0][0] > 0:
                messages.error(request, "O email já está em uso.")
                return render(request, 'sger/register.html')

            # Verifica se este é o primeiro usuário (Master)
            is_master = False
            sql_count_users = "SELECT COUNT(*) FROM auth_user"
            user_count = execute_query(sql_count_users)[0][0]
            if user_count == 0:
                is_master = True

            # Define a data de criação (date_joined)
            date_joined = datetime.now()

            # Insere o usuário no banco de dados
            sql_insert_user = """
                INSERT INTO auth_user 
                (username, email, password, is_superuser, is_staff, is_active, first_name, last_name, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            execute_query(sql_insert_user, [username, email, hashed_password, is_master, is_master, True, first_name, last_name, date_joined])

            # Recupera IDs para associar o usuário ao grupo correto
            group_name = 'Master' if is_master else 'Cliente'
            sql_get_user_id = "SELECT id FROM auth_user WHERE username = %s"
            user_id = execute_query(sql_get_user_id, [username])[0][0]
            sql_get_group_id = "SELECT id FROM auth_group WHERE name = %s"
            group_id = execute_query(sql_get_group_id, [group_name])[0][0]

            # Insere a associação do usuário ao grupo
            sql_insert_group = """
                INSERT INTO auth_user_groups (user_id, group_id)
                VALUES (%s, %s)
            """
            execute_query(sql_insert_group, [user_id, group_id])

            # Mensagem de sucesso
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')

        except Exception as e:
            # Tratamento de erro
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return render(request, 'sger/register.html')

    return render(request, 'sger/register.html')

def clientes_view(request):
    return render(request, 'sger/clientes/clientes.html')  

@login_required
def projetos_view(request):
    def execute_query(sql, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    user_groups = request.user.groups.values_list('name', flat=True)
    is_admin = 'Master' in user_groups or 'Administradores' in user_groups
    is_client = 'Cliente' in user_groups

    if request.method == 'POST' and is_admin:
        # Validação dos campos do formulário
        project_name = request.POST.get('project_name', '').strip()
        project_description = request.POST.get('project_description', '').strip()
        project_start_date = request.POST.get('project_start_date', '').strip()
        project_end_date = request.POST.get('project_end_date', '').strip()
        client_id = request.POST.get('client_id')

        if not project_name or not client_id:
            messages.error(request, "Por favor, preencha os campos obrigatórios.")
            return redirect('projetos')

        # Insere no banco
        sql_insert = """
        INSERT INTO Projeto (Nome, Descricao, Data_Inicio, Data_Termino, Cliente_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            execute_query(sql_insert, [project_name, project_description, project_start_date, project_end_date, client_id])
            messages.success(request, "Projeto cadastrado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar projeto: {e}")
        return redirect('projetos')

    # Lógica para listar projetos
    if is_client:
        sql_select = """
        SELECT Projeto.ID, Projeto.Nome, Projeto.Descricao, Projeto.Data_Inicio, Projeto.Data_Termino, Cliente.Nome AS Cliente_Nome
        FROM Projeto
        LEFT JOIN Cliente ON Projeto.Cliente_ID = Cliente.ID
        WHERE Cliente.ID = %s
        ORDER BY Projeto.Nome
        """
        projects = execute_query(sql_select, [request.user.id])
    else:
        sql_select = """
        SELECT Projeto.ID, Projeto.Nome, Projeto.Descricao, Projeto.Data_Inicio, Projeto.Data_Termino, Cliente.Nome AS Cliente_Nome
        FROM Projeto
        LEFT JOIN Cliente ON Projeto.Cliente_ID = Cliente.ID
        ORDER BY Projeto.Nome
        """
        projects = execute_query(sql_select)

    # Busca todos os clientes para o formulário
    clients = []
    if is_admin:
        sql_clients = "SELECT ID, Nome FROM Cliente ORDER BY Nome"
        clients = execute_query(sql_clients)

    context = {
        'projects': projects,
        'clients': clients,
        'is_admin': is_admin,
    }
    return render(request, 'sger/projetos/projetos.html', context)

@login_required
def tarefas_view(request):
    def execute_query(sql, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    user_groups = request.user.groups.values_list('name', flat=True)
    is_admin = 'Master' in user_groups or 'Administradores' in user_groups
    is_client = 'Cliente' in user_groups

    if request.method == 'POST' and is_admin:
        # Validação dos campos do formulário
        task_description = request.POST.get('task_description', '').strip()
        task_start_date = request.POST.get('task_start_date', '').strip()
        task_end_date = request.POST.get('task_end_date', '').strip()
        task_status = request.POST.get('task_status', '').strip()
        project_id = request.POST.get('project_id')

        if not task_description or not project_id:
            messages.error(request, "Por favor, preencha os campos obrigatórios.")
            return redirect('tarefas')

        # Insere no banco
        sql_insert = """
        INSERT INTO Tarefa (Descricao, Data_Inicio, Data_Termino, Status, Projeto_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            execute_query(sql_insert, [task_description, task_start_date, task_end_date, task_status, project_id])
            messages.success(request, "Tarefa cadastrada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar tarefa: {e}")
        return redirect('tarefas')

    # Lógica para listar tarefas
    if is_client:
        sql_select = """
        SELECT Tarefa.ID, Tarefa.Descricao, Tarefa.Data_Inicio, Tarefa.Data_Termino, Tarefa.Status, Projeto.Nome AS Projeto_Nome
        FROM Tarefa
        LEFT JOIN Projeto ON Tarefa.Projeto_ID = Projeto.ID
        WHERE Projeto.Cliente_ID = %s
        ORDER BY Tarefa.Descricao
        """
        tasks = execute_query(sql_select, [request.user.id])
    else:
        sql_select = """
        SELECT Tarefa.ID, Tarefa.Descricao, Tarefa.Data_Inicio, Tarefa.Data_Termino, Tarefa.Status, Projeto.Nome AS Projeto_Nome
        FROM Tarefa
        LEFT JOIN Projeto ON Tarefa.Projeto_ID = Projeto.ID
        ORDER BY Tarefa.Descricao
        """
        tasks = execute_query(sql_select)

    # Busca todos os projetos para o formulário
    projects = []
    if is_admin:
        sql_projects = "SELECT ID, Nome FROM Projeto ORDER BY Nome"
        projects = execute_query(sql_projects)

    context = {
        'tasks': tasks,
        'projects': projects,
        'is_admin': is_admin,
    }
    return render(request, 'sger/tarefas/tarefas.html', context)


def recursos_view(request):
    return render(request, 'sger/recursos/recursos.html') 
def contatos_view(request):
    return render(request, 'sger/contatos/contatos.html')

def funcionarios_view(request):
    return render(request, 'sger/funcionarios/funcionarios.html')
def alocacoes_view(request):
    return render(request, 'sger/alocacoes/alocacoes.html')
def departamentos_view(request):
    return render(request, 'sger/departamentos/departamentos.html')



@login_required
def usuarios_view(request):
    usuarios = User.objects.all()
    grupos = Group.objects.exclude(name="Master")  # Também exclui "Master" da seleção de grupos

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_name = request.POST.get("group")

        # Valida se o user_id é válido
        if not user_id or not user_id.isdigit():
            messages.error(request, "ID de usuário inválido.")
            return redirect("usuarios")

        # Recupera o usuário e o grupo
        try:
            user = User.objects.get(id=user_id)

            # Evita que o grupo Master seja alterado, mesmo se tentarem manualmente
            if user.groups.filter(name="Master").exists():
                messages.error(request, "Não é permitido alterar o grupo do usuário Master.")
                return redirect("usuarios")

            group = Group.objects.get(name=group_name)
            user.groups.clear()  # Remove todos os grupos
            user.groups.add(group)  # Adiciona o novo grupo
            messages.success(request, f"Grupo do usuário {user.username} atualizado com sucesso.")

        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
        except Group.DoesNotExist:
            messages.error(request, "Grupo selecionado não existe.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {e}")

        return redirect("usuarios")

    return render(request, "sger/usuarios/usuarios.html", {"usuarios": usuarios, "grupos": grupos})
