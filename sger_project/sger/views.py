import re

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from sger.utils.database import executar_consulta
from django.db import connection
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from datetime import datetime
from datetime import datetime
from sger.utils.decorators import role_required

@login_required
def home_view(request):
    storage = messages.get_messages(request)
    storage.used = True
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)

    context = {
        'is_master': 'Master' in user_groups,
        'is_admin': 'Administradores' in user_groups or 'Master' in user_groups,
        'is_employee': 'Funcionarios' in user_groups,
        'is_client': 'Cliente' in user_groups,
    }
    return render(request, 'sger/home.html', context)

def execute_query(sql, params=None):
    """
    Função auxiliar para executar consultas SQL brutas.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()
        
#---------------------------------#
# Funções para autenticação
def login_view(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        identifier = request.POST.get('username')  # Pode ser username ou email
        password = request.POST.get('password')

        User = get_user_model()  # Obtém o modelo de usuário atual

        try:
            # Verifica se o identificador é um email válido
            if '@' in identifier:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username  # Obtém o nome de usuário para autenticação
            else:
                username = identifier  # Considera como nome de usuário
        except User.DoesNotExist:
            username = None

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect('home')  # Redireciona para a home
        else:
            messages.error(request, "Usuário ou senha incorretos. Tente novamente.")

    return render(request, 'sger/login.html')

def logout_view(request):
    request.session.flush()  # Limpa a sessão do usuário
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, 'Logout realizado com sucesso!')
    logout(request)
    return redirect('login')

def validate_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)  # Remove qualquer caractere não numérico
    if len(cnpj) != 14:
        raise ValueError("O CNPJ deve conter exatamente 14 dígitos.")
    return cnpj

def validate_cpf_cnpj(value, is_cpf=True):
    """
    Valida CPF ou CNPJ. Retorna True se for válido, False caso contrário.
    """
    value = format_cpf_cnpj(value)
    if is_cpf and len(value) == 11:
        return True  # Aqui você pode implementar validação mais robusta
    if not is_cpf and len(value) == 14:
        return True  # Aqui você pode implementar validação mais robusta
    return False

def register_view(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        try:
            # Captura dados do formulário
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            full_name = request.POST.get('full_name', '').strip()  # Captura nome completo
            cnpj = request.POST.get('cnpj', '').strip()
            address = request.POST.get('endereco', '').strip()
            phone = request.POST.get('telefone', '').strip()
            hashed_password = make_password(password)

            # Divide o nome completo em primeiro nome e último nome
            first_name, last_name = (full_name.split(' ', 1) + [''])[:2]

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

            # Se o grupo for Cliente, insere os dados na tabela Cliente
            if group_name == 'Cliente':
                sql_insert_client = """
                    INSERT INTO Cliente (Nome, CNPJ, Endereco, Telefone)
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(sql_insert_client, [full_name, cnpj, address, phone])

            # Mensagem de sucesso
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')

        except Exception as e:
            # Tratamento de erro
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return render(request, 'sger/register.html')

    return render(request, 'sger/register.html')

#---------------------------------#
# Funções para gerenciamento de projetos

@login_required
def projetos_view(request):
    
    """
    Lista e gerencia os projetos, filtrando-os dependendo do tipo de usuário.
    """
    storage = messages.get_messages(request)
    storage.used = True

    # Verifica se o usuário pertence ao grupo 'Cliente'
    is_client = request.user.groups.filter(name='Cliente').exists()

    # Consulta a lista de projetos com filtro para clientes ou sem filtro para admins/masters
    if is_client:
        sql_select_projects = """
            SELECT p.ID, p.Nome, p.Descricao, DATE_FORMAT(p.Data_Inicio, '%%d/%%m/%%Y'), 
                   DATE_FORMAT(p.Data_Termino, '%%d/%%m/%%Y'), c.Nome 
            FROM Projeto p 
            INNER JOIN Cliente c ON p.Cliente_ID = c.ID
            WHERE c.Nome = %s
            ORDER BY p.Data_Inicio
        """
        projects = execute_query(sql_select_projects, [request.user.get_full_name()])
    else:
        sql_select_projects = """
            SELECT p.ID, p.Nome, p.Descricao, DATE_FORMAT(p.Data_Inicio, '%%d/%%m/%%Y'), 
                   DATE_FORMAT(p.Data_Termino, '%%d/%%m/%%Y'), c.Nome 
            FROM Projeto p 
            INNER JOIN Cliente c ON p.Cliente_ID = c.ID
            ORDER BY p.Data_Inicio
        """
        projects = execute_query(sql_select_projects)

    # Para admins, também enviar a lista de clientes para cadastro de novos projetos
    clients = []
    if not is_client:
        sql_select_clients = """
            SELECT ID, Nome 
            FROM Cliente 
            ORDER BY Nome
        """
        clients = execute_query(sql_select_clients)

    if request.method == 'POST' and not is_client:
        # Lida com o cadastro de novos projetos
        project_name = request.POST.get('project_name')
        client_id = request.POST.get('client_id')
        project_description = request.POST.get('project_description')
        project_start_date = request.POST.get('project_start_date')
        project_end_date = request.POST.get('project_end_date')

        sql_insert_project = """
            INSERT INTO Projeto (Nome, Descricao, Data_Inicio, Data_Termino, Cliente_ID) 
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(sql_insert_project, [project_name, project_description, project_start_date, project_end_date, client_id])
        messages.success(request, "Projeto cadastrado com sucesso!")
        return redirect('projetos')

    return render(request, 'sger/projetos/projetos.html', {
        'projects': projects,
        'clients': clients,
        'is_client': is_client,
    })

@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def edit_project_view(request, project_id):
    storage = messages.get_messages(request)
    storage.used = True
    """
    Edita um projeto existente.
    """
    # Consulta o projeto pelo ID
    sql_select_project = """
        SELECT ID, Nome, Descricao, Data_Inicio, Data_Termino, Cliente_ID 
        FROM Projeto 
        WHERE ID = %s
    """
    project = execute_query(sql_select_project, [project_id])

    if not project:
        messages.error(request, "Projeto não encontrado.")
        return redirect('projetos')

    # Consulta a lista de clientes
    sql_select_clients = """
        SELECT ID, Nome 
        FROM Cliente 
        ORDER BY Nome
    """
    clients = execute_query(sql_select_clients)

    if request.method == 'POST':
        # Captura os dados do formulário
        name = request.POST.get('project_name')
        description = request.POST.get('project_description')
        start_date = request.POST.get('project_start_date')
        end_date = request.POST.get('project_end_date')
        client_id = request.POST.get('client_id')

        # Atualiza o projeto no banco de dados
        sql_update = """
            UPDATE Projeto
            SET Nome = %s, Descricao = %s, Data_Inicio = %s, Data_Termino = %s, Cliente_ID = %s
            WHERE ID = %s
        """
        execute_query(sql_update, [name, description, start_date, end_date, client_id, project_id])
        messages.success(request, "Projeto atualizado com sucesso!")
        return redirect('projetos')

    # Envia os dados do projeto e a lista de clientes para o template
    return render(request, 'sger/projetos/edit_project.html', {
        'project': {
            'id': project[0][0],
            'name': project[0][1],
            'description': project[0][2],
            'start_date': project[0][3],
            'end_date': project[0][4],
            'client_id': project[0][5],
        },
        'clients': clients,
    })


@login_required
@role_required('Master', 'Administradores')
def delete_project_view(request, project_id):
    storage = messages.get_messages(request)
    storage.used = True
    """
    Exclui um projeto existente.
    """
    sql_delete = "DELETE FROM Projeto WHERE ID = %s"
    execute_query(sql_delete, [project_id])
    messages.success(request, "Projeto excluído com sucesso!")
    return redirect('projetos')



#---------------------------------#
# Funções para gerenciamento de usuários

@login_required
@role_required('Master')
def usuarios_view(request):
    """
    Gerencia usuários e permite alterar grupo, reutilizando dados existentes da tabela Cliente.
    """
    storage = messages.get_messages(request)
    storage.used = True
    usuarios = User.objects.all()
    grupos = Group.objects.exclude(name="Master")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_name = request.POST.get("group")

        try:
            user = User.objects.get(id=user_id)

            # Impedir alteração do grupo do Master
            if user.groups.filter(name="Master").exists():
                messages.error(request, "Não é permitido alterar o grupo do usuário Master.")
                return redirect("usuarios")

            # Recuperar dados existentes da tabela Cliente
            nome_completo = f"{user.first_name} {user.last_name}"
            cliente_data = execute_query(
                "SELECT CNPJ, Telefone FROM Cliente WHERE Nome = %s",
                [nome_completo]
            )

            # Remove o usuário de tabelas anteriores
            remove_user_from_previous_table(user)

            # Atualizar grupo
            group = Group.objects.get(name=group_name)
            user.groups.clear()
            user.groups.add(group)

            # Adicionar às tabelas apropriadas com dados reutilizados
            if group_name == "Funcionarios":
                if cliente_data:
                    cnpj, telefone = cliente_data[0]
                    add_to_funcionario(user, cnpj[:11], telefone)  # CPF pode ser derivado do CNPJ
                else:
                    messages.error(request, "Dados do cliente não encontrados para promover a funcionário.")
            elif group_name == "Cliente":
                if cliente_data:
                    cnpj, telefone = cliente_data[0]
                    add_to_cliente(user, cnpj, telefone)
                else:
                    messages.error(request, "Erro ao mover para Cliente. Dados incompletos.")

            messages.success(request, f"Grupo do usuário {user.username} atualizado com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro: {e}")
        return redirect("usuarios")

    return render(request, "sger/usuarios/usuarios.html", {"usuarios": usuarios, "grupos": grupos})


def remove_user_from_previous_table(user):
    """
    Remove o usuário das tabelas Cliente e Funcionario, caso exista.
    """
    nome_completo = f"{user.first_name} {user.last_name}"
    execute_query("DELETE FROM Cliente WHERE Nome = %s", [nome_completo])
    execute_query("DELETE FROM Funcionario WHERE Nome = %s", [nome_completo])


def add_to_funcionario(user, cpf, telefone):
    """
    Adiciona o usuário à tabela Funcionarios.
    """
    sql_insert_funcionario = """
        INSERT INTO Funcionario (Nome, CPF, Data_Contratacao, Telefone)
        VALUES (%s, %s, CURDATE(), %s)
    """
    nome_completo = f"{user.first_name} {user.last_name}"
    execute_query(sql_insert_funcionario, [nome_completo, cpf, telefone])


def add_to_cliente(user, cnpj, telefone):
    """
    Adiciona o usuário à tabela Clientes.
    """
    sql_insert_cliente = """
        INSERT INTO Cliente (Nome, CNPJ, Endereco, Telefone)
        VALUES (%s, %s, %s, %s)
    """
    nome_completo = f"{user.first_name} {user.last_name}"
    endereco = "Endereço Padrão"
    execute_query(sql_insert_cliente, [nome_completo, cnpj, endereco, telefone])


#---------------------------------#
# Funções para gerenciamento de clientes

@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def clients_list(request):
    """
    Lista todos os clientes cadastrados no sistema.
    """
    sql_select = """
        SELECT ID, Nome, CNPJ, Endereco, Telefone 
        FROM Cliente
        ORDER BY Nome
    """
    clients = execute_query(sql_select)

    # Aplica a formatação diretamente na view
    formatted_clients = []
    for client in clients:
        formatted_cnpj = (
            f"{client[2][:2]}.{client[2][2:5]}.{client[2][5:8]}/{client[2][8:12]}-{client[2][12:]}"
            if client[2] and len(client[2]) == 14
            else client[2]
        )
        formatted_phone = (
            f"({client[4][:2]}) {client[4][2:7]}-{client[4][7:]}"
            if client[4] and len(client[4]) == 11
            else f"({client[4][:2]}) {client[4][2:6]}-{client[4][6:]}"
            if client[4] and len(client[4]) == 10
            else client[4]
        )
        formatted_clients.append(
            (client[0], client[1], formatted_cnpj, client[3], formatted_phone)
        )

    return render(request, 'sger/clientes/clients_list.html', {'clients': formatted_clients})



@login_required
@role_required('Master', 'Administradores')
def edit_client_view(request, client_id):
    storage = messages.get_messages(request)
    storage.used = True
    """
    Permite editar as informações de um cliente específico.
    """
    # Busca os dados do cliente
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente WHERE ID = %s"
    client_data = execute_query(sql_select, [client_id])

    if not client_data:
        messages.error(request, "Cliente não encontrado!")
        return redirect('clients_list')

    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')

        try:
            cnpj = validate_cnpj(cnpj)  # Validação do CNPJ
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('edit_client', client_id=client_id)
        
        # Atualiza o cliente no banco de dados
        sql_update = """
        UPDATE Cliente
        SET Nome = %s, CNPJ = %s, Endereco = %s, Telefone = %s
        WHERE ID = %s
        """
        execute_query(sql_update, [nome, cnpj, endereco, telefone, client_id])
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('clients_list')

    # Passa os dados do cliente para o template
    client = client_data[0]
    return render(request, 'sger/clientes/edit_client.html', {'client': client})


@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def clients_search_view(request):
    storage = messages.get_messages(request)
    storage.used = True
    """
    Permite buscar clientes por Nome, CNPJ, Endereço ou Telefone.
    """
    search_term = request.GET.get('search_term', '').strip()

    sql_select = """
        SELECT ID, Nome, CNPJ, Endereco, Telefone 
        FROM Cliente
        WHERE Nome LIKE %s OR CNPJ LIKE %s OR Endereco LIKE %s OR Telefone LIKE %s
        ORDER BY Nome
    """
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']
    clients = execute_query(sql_select, parametros)
    return render(request, 'sger/clientes/clients_list.html', {'clients': clients})

#---------------------------------#
# Funções para gerenciamento de departamentos
@login_required
@role_required('Master', 'Administradores')
def department_register_view(request):
    """
    Registra um novo departamento e lista os existentes.
    """
    if request.method == 'POST':
        department_name = request.POST.get('entry_department_name')
        responsible_employee_id = request.POST.get('entry_responsible_employee')

        # Insere o novo departamento na tabela
        sql_insert = """
        INSERT INTO Departamento (Nome, Responsavel_ID)
        VALUES (%s, %s)
        """
        execute_query(sql_insert, [department_name, responsible_employee_id])

        messages.success(request, "Departamento cadastrado com sucesso!")
        return redirect('department_register')

    # Busca todos os departamentos para exibição na tabela
    sql_select_departments = """
        SELECT Departamento.ID, Departamento.Nome, Funcionario.Nome AS Responsavel
        FROM Departamento
        LEFT JOIN Funcionario ON Departamento.Responsavel_ID = Funcionario.ID
        ORDER BY Departamento.Nome
    """
    departments = execute_query(sql_select_departments)

    # Busca todos os funcionários para preencher o campo de seleção no formulário
    sql_select_employees = "SELECT ID, Nome FROM Funcionario ORDER BY Nome"
    employees = execute_query(sql_select_employees)

    # Passa os dados para o template
    context = {
        'departments': departments,
        'employees': employees,
    }
    return render(request, 'sger/departamentos/department_register.html', context)


@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def department_list_view(request):
    """
    Lista todos os departamentos com seus responsáveis.
    """
    sql_select = """
    SELECT 
        Departamento.ID, 
        Departamento.Nome AS Departamento_Nome, 
        Funcionario.Nome AS Funcionario_Responsavel
    FROM 
        Departamento
    LEFT JOIN 
        Funcionario ON Departamento.Responsavel_ID = Funcionario.ID
    ORDER BY 
        Departamento.Nome
    """
    departments = execute_query(sql_select)
    user_groups = request.user.groups.values_list('name', flat=True)
    is_admin_or_master = 'Master' in user_groups or 'Administradores' in user_groups


    context = {
        'departments': departments,
        'is_admin_or_master': is_admin_or_master,
    }
    return render(request, 'sger/departamentos/department_list.html', context)


@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def departments_search_view(request):
    """
    Pesquisa departamentos por nome ou responsável.
    """
    search_term = request.GET.get('search_term', '').strip()

    sql_select = """
    SELECT 
        Departamento.ID, 
        Departamento.Nome AS Departamento_Nome, 
        Funcionario.Nome AS Funcionario_Responsavel
    FROM 
        Departamento
    LEFT JOIN 
        Funcionario ON Departamento.Responsavel_ID = Funcionario.ID
    WHERE 
        Departamento.Nome LIKE %s OR Funcionario.Nome LIKE %s
    ORDER BY 
        Departamento.Nome
    """
    parametros = [f'%{search_term}%', f'%{search_term}%']
    departments = execute_query(sql_select, parametros)

    context = {
        'departments': departments,
    }
    return render(request, 'sger/departamentos/department_list.html', context)


@login_required
@role_required('Master', 'Administradores')
def delete_department_view(request, id):
    """
    Exclui um departamento existente.
    """
    # Verifica se o departamento existe
    sql_select = "SELECT ID FROM Departamento WHERE ID = %s"
    department_exists = execute_query(sql_select, [id])

    if not department_exists:
        messages.error(request, "Departamento não encontrado!")
        return redirect('department_list')

    # Deleta o departamento
    sql_delete = "DELETE FROM Departamento WHERE ID = %s"
    execute_query(sql_delete, [id])

    messages.success(request, "Departamento deletado com sucesso!")
    return redirect('department_list')


@login_required
@role_required('Master', 'Administradores')
def edit_department_view(request, id):
    """
    Edita os dados de um departamento existente.
    """
    # Busca os dados do departamento
    sql_select = """
    SELECT 
        Departamento.ID, 
        Departamento.Nome, 
        Departamento.Responsavel_ID 
    FROM 
        Departamento 
    WHERE 
        ID = %s
    """
    department_data = execute_query(sql_select, [id])

    if not department_data:
        messages.error(request, "Departamento não encontrado!")
        return redirect('department_list')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        funcionario_responsavel_id = request.POST.get('responsible')

        # Atualiza os dados do departamento
        sql_update = """
        UPDATE Departamento
        SET Nome = %s, Responsavel_ID = %s
        WHERE ID = %s
        """
        execute_query(sql_update, [nome, funcionario_responsavel_id, id])

        messages.success(request, "Departamento atualizado com sucesso!")
        return redirect('department_list')

    # Busca a lista de funcionários para o dropdown
    sql_select_employees = "SELECT ID, Nome FROM Funcionario ORDER BY Nome"
    employees = execute_query(sql_select_employees)

    context = {
        'department': {
            'id': department_data[0][0],
            'name': department_data[0][1],
            'responsible_id': department_data[0][2],
        },
        'employees': employees,
    }
    return render(request, 'sger/departamentos/department_edit.html', context)
#---------------------------------#
# Funções para gerenciamento de contatos

@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def contacts_view(request):
    """
    Lista e pesquisa todos os contatos de usuários cadastrados no sistema.
    """
    search_term = request.GET.get('search_term', '').strip()

    # Consulta SQL ajustada para combinar dados de Cliente e auth_user
    sql_select_contacts = """
    SELECT 
        Cliente.ID, 
        Cliente.Nome AS first_name,
        auth_user.email,
        Cliente.Telefone
    FROM 
        Cliente
    LEFT JOIN 
        auth_user ON Cliente.Nome = CONCAT(auth_user.first_name, ' ', auth_user.last_name)
    WHERE 
        Cliente.Nome LIKE %s OR 
        auth_user.email LIKE %s OR 
        Cliente.Telefone LIKE %s
    ORDER BY 
        Cliente.Nome
    """

    # Parâmetros para a consulta SQL
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']
    contacts = execute_query(sql_select_contacts, parametros)

    # Renderiza os contatos encontrados
    context = {
        'contacts': contacts,
        'search_term': search_term,
    }
    return render(request, 'sger/contatos/contacts.html', context)




@login_required
@role_required('Master', 'Administradores', 'Funcionarios')
def funcionarios_view(request):
    """
    Lista e pesquisa os funcionários cadastrados no sistema.
    Funcionários só podem ver os próprios dados.
    Master e Administradores podem gerenciar todos os registros.
    """
    search_term = request.GET.get('search_term', '').strip()
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)

    if 'Funcionarios' in user_groups:
        # Funcionário visualiza apenas seus próprios dados
        sql_query = """
            SELECT 
                Funcionario.ID, Funcionario.Nome, Funcionario.CPF, 
                DATE_FORMAT(Funcionario.Data_Contratacao, '%%d/%%m/%%Y') AS Data_Contratacao,
                Funcionario.Telefone
            FROM Funcionario
            WHERE Funcionario.Nome = %s
        """
        funcionarios = execute_query(sql_query, [user.get_full_name()])
    else:
        # Master e Administradores têm acesso a todos os funcionários
        sql_query = """
            SELECT 
                Funcionario.ID, Funcionario.Nome, Funcionario.CPF, 
                DATE_FORMAT(Funcionario.Data_Contratacao, '%%d/%%m/%%Y') AS Data_Contratacao,
                Funcionario.Telefone
            FROM Funcionario
            WHERE 
                Funcionario.Nome LIKE %s OR 
                Funcionario.CPF LIKE %s OR 
                Funcionario.Telefone LIKE %s
            ORDER BY Funcionario.Nome
        """
        parametros = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
        funcionarios = execute_query(sql_query, parametros)

    # Renderiza a lista de funcionários
    return render(request, 'sger/funcionarios/funcionarios.html', {
        'funcionarios': funcionarios,
        'search_term': search_term,
        'is_employee': 'Funcionarios' in user_groups,
        'is_admin_or_master': 'Master' in user_groups or 'Administradores' in user_groups
    })


@login_required
@role_required('Master', 'Administradores')
def cadastrar_funcionario_view(request):
    """
    Cadastra um funcionário utilizando os dados dos clientes existentes.
    Apenas clientes não cadastrados como funcionários podem ser promovidos.
    """
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')

        try:
            # Busca os dados do cliente
            sql_get_cliente = """
                SELECT Nome, Telefone, CNPJ 
                FROM Cliente 
                WHERE ID = %s
            """
            cliente_data = execute_query(sql_get_cliente, [cliente_id])

            if not cliente_data:
                messages.error(request, "Cliente não encontrado.")
                return redirect('cadastrar_funcionario')

            nome, telefone, cnpj = cliente_data[0]
            cpf = cnpj[:11]  # Extrai CPF do CNPJ como placeholder
            data_contratacao = datetime.now().date()

            # Verifica duplicidade na tabela Funcionario
            sql_check_funcionario = "SELECT COUNT(*) FROM Funcionario WHERE Nome = %s"
            if execute_query(sql_check_funcionario, [nome])[0][0] > 0:
                messages.error(request, "Este cliente já é um funcionário.")
                return redirect('cadastrar_funcionario')

            # Insere o cliente como funcionário
            sql_insert_funcionario = """
                INSERT INTO Funcionario (Nome, CPF, Data_Contratacao, Telefone) 
                VALUES (%s, %s, %s, %s)
            """
            execute_query(sql_insert_funcionario, [nome, cpf, data_contratacao, telefone])

            # Atualiza o grupo do usuário no sistema
            sql_update_user_group = """
                UPDATE auth_user_groups 
                SET group_id = (
                    SELECT id FROM auth_group WHERE name = 'Funcionarios'
                ) 
                WHERE user_id = (
                    SELECT id FROM auth_user 
                    WHERE CONCAT(first_name, ' ', last_name) = %s
                )
            """
            execute_query(sql_update_user_group, [nome])

            messages.success(request, f"Funcionário '{nome}' cadastrado com sucesso!")
            return redirect('funcionarios')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao cadastrar o funcionário: {e}")
            return redirect('cadastrar_funcionario')

    # Busca todos os clientes não cadastrados como funcionários
    sql_get_clientes = """
        SELECT Cliente.ID, Cliente.Nome, Cliente.Telefone 
        FROM Cliente 
        WHERE Cliente.Nome NOT IN (SELECT Nome FROM Funcionario)
        ORDER BY Cliente.Nome
    """
    clientes = execute_query(sql_get_clientes)

    return render(request, 'sger/funcionarios/cadastrar_funcionario.html', {
        'clientes': clientes,
    })


@login_required
@role_required('Master', 'Administradores')
def excluir_funcionario_view(request, funcionario_id):
    """
    Exclui um funcionário e reatribui o grupo para Cliente.
    """
    try:
        # Busca o nome do funcionário para atualizações
        sql_get_funcionario = "SELECT Nome FROM Funcionario WHERE ID = %s"
        funcionario_data = execute_query(sql_get_funcionario, [funcionario_id])

        if not funcionario_data:
            messages.error(request, "Funcionário não encontrado.")
            return redirect('funcionarios')

        nome = funcionario_data[0][0]

        # Remove da tabela Funcionario
        sql_delete_funcionario = "DELETE FROM Funcionario WHERE ID = %s"
        execute_query(sql_delete_funcionario, [funcionario_id])

        # Atualiza o grupo do usuário no sistema para Cliente
        sql_update_user_group = """
            UPDATE auth_user_groups 
            SET group_id = (
                SELECT id FROM auth_group WHERE name = 'Cliente'
            ) 
            WHERE user_id = (
                SELECT id FROM auth_user 
                WHERE CONCAT(first_name, ' ', last_name) = %s
            )
        """
        execute_query(sql_update_user_group, [nome])

        messages.success(request, f"Funcionário '{nome}' excluído com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao excluir funcionário: {e}")

    return redirect('funcionarios')



def recursos_view(request):
    return render(request, 'sger/recursos/recursos.html') 

def tarefas_view(request):
    return render(request, 'sger/tarefas/tarefas.html')

def alocacoes_view(request):
    return render(request, 'sger/alocacoes/alocacoes.html')

