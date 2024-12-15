from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import authenticate, login
from clients.decorators import role_required




def executar_consulta(sql, parametros=None):
    """
    Função auxiliar para executar consultas SQL brutas.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, parametros or [])
        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()


def home(request):
    return render(request, 'clients/home.html')

@role_required('Admin', 'Funcionario')
@login_required
def clients_list(request):
    # Salva o registro do cliente
    if request.method == 'POST':
        client_name = request.POST.get('entry_client_name')
        client_cnpj = request.POST.get('clean_cnpj')
        client_address = request.POST.get('entry_client_address')
        client_phone = request.POST.get('entry_client_phone')

        # Insere o novo cliente na tabela
        sql_insert = """
        INSERT INTO Cliente (Nome, CNPJ, Endereco, Telefone)
        VALUES (%s, %s, %s, %s)
        """
        executar_consulta(sql_insert, [client_name, client_cnpj, client_address, client_phone])

    # Busca todos os clientes para exibir na página
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente ORDER BY Nome"
    clients = executar_consulta(sql_select)

    return render(request, 'clients/clients_list.html', {'clients': clients})

@role_required('Funcionario', 'Admin')
@login_required
def clients_register_view(request):
    # Consulta para buscar todos os clientes
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente ORDER BY Nome"
    clients = executar_consulta(sql_select)

    return render(request, 'clients/clients_register.html', {'clientsList': {'clients': clients}})

@role_required('Admin', 'Funcionario')
@login_required
def clients_search_view(request):
    # Pega o termo de pesquisa (caso exista)
    search_term = request.GET.get('search_term', '').strip()

    # Consulta para buscar todos os clientes, ou aplicar filtro de pesquisa se necessário
    sql_select = """
        SELECT ID, Nome, CNPJ, Endereco, Telefone 
        FROM Cliente
        WHERE Nome LIKE %s OR CNPJ LIKE %s OR Endereco LIKE %s OR Telefone LIKE %s
        ORDER BY Nome
    """
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']
    clients = executar_consulta(sql_select, parametros)

    return render(request, 'clients/clients_list.html', {'clients': clients})

@role_required('Admin')
@login_required
def delete_clients_view(request, id):
    # Consulta SQL para verificar se o cliente existe
    sql_select = "SELECT ID FROM Cliente WHERE ID = %s"
    client_exists = executar_consulta(sql_select, [id])

    if not client_exists:
        messages.error(request, "Cliente não encontrado!")
        return redirect('clients_list')

    # Consulta SQL para deletar o cliente
    sql_delete = "DELETE FROM Cliente WHERE ID = %s"
    executar_consulta(sql_delete, [id])

    messages.info(request, 'Cliente deletado com sucesso!')
    return redirect('clients_list')

@role_required('Funcionario', 'Admin')
@login_required
def edit_client_view(request, id):
    # Consulta SQL para buscar os dados do cliente
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente WHERE ID = %s"
    client_data = executar_consulta(sql_select, [id])

    if not client_data:
        messages.error(request, "Cliente não encontrado!")
        return redirect('clients_list')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')

        sql_update = """
        UPDATE Cliente
        SET Nome = %s, CNPJ = %s, Endereco = %s, Telefone = %s
        WHERE ID = %s
        """
        executar_consulta(sql_update, [nome, cnpj, endereco, telefone, id])
        messages.info(request, 'Cliente atualizado com sucesso!')
        return redirect('clients_list')

    client = client_data[0]  # Extraindo os dados do cliente da lista
    return render(request, 'clients/edit_client.html', {'client': client})

@role_required('Admin')
@login_required
def assign_role_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')

        # Verifica se o usuário existe
        sql_check = "SELECT id FROM auth_user WHERE id = %s"
        user_exists = executar_consulta(sql_check, [user_id])

        if not user_exists:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('assign_role')

        # Atualiza o papel do usuário
        sql_update_role = """
        UPDATE UserRoles
        SET role = %s
        WHERE user_id = %s
        """
        executar_consulta(sql_update_role, [new_role, user_id])

        messages.success(request, f'Papel do usuário atualizado para {new_role}!')
        return redirect('assign_role')

    # Busca todos os usuários para exibir na página
    sql_users = "SELECT id, username FROM auth_user"
    users = executar_consulta(sql_users)
    
    # Busca papéis atuais dos usuários
    sql_roles = "SELECT user_id, role FROM UserRoles"
    roles = executar_consulta(sql_roles)

    return render(request, 'assign_role.html', {'users': users, 'roles': roles})


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login bem-sucedido
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial ou outra rota
        else:
            # Falha no login: mensagem de erro
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    # Renderiza a página de login com os dados inseridos (exceto senha)
    return render(request, 'login.html', {
        'username': request.POST.get('username', ''),
    })


# Registro
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('register')

        # Verifica se o banco está vazio (primeiro usuário será master)
        sql_check_master = "SELECT COUNT(*) FROM auth_user"
        user_count = executar_consulta(sql_check_master)[0][0]

        # Verifica se o usuário já existe
        sql_check = "SELECT id FROM auth_user WHERE username = %s"
        user_exists = executar_consulta(sql_check, [username])

        if user_exists:
            messages.error(request, 'Usuário já existe.')
            return redirect('register')

        # Insere o novo usuário no banco
        hashed_password = make_password(password)
        date_joined = datetime.now()

        if user_count == 0:  # Primeiro usuário (Admin Master)
            sql_insert = """
            INSERT INTO auth_user (username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            executar_consulta(sql_insert, [username, hashed_password, first_name, last_name, email, True, True, True, date_joined])
            messages.success(request, 'Registro realizado com sucesso! Você é o administrador master.')
        else:  # Demais usuários (Clientes)
            sql_insert = """
            INSERT INTO auth_user (username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            executar_consulta(sql_insert, [username, hashed_password, first_name, last_name, email, False, False, True, date_joined])

            # Adiciona o papel de cliente ao usuário na tabela UserRoles
            sql_role_insert = """
            INSERT INTO UserRoles (user_id, role)
            SELECT id, 'Cliente' FROM auth_user WHERE username = %s
            """
            executar_consulta(sql_role_insert, [username])

            messages.success(request, 'Registro realizado com sucesso!')

        # Login automático
        sql_get_user = "SELECT id FROM auth_user WHERE username = %s"
        user_id = executar_consulta(sql_get_user, [username])[0][0]
        request.session['user_id'] = user_id

        messages.success(request, 'Login automático realizado com sucesso!')
        return redirect('home')

    return render(request, 'register.html')



def admin_only_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Você precisa estar logado para acessar esta página.')
        return redirect('login')

    # Verifica se o usuário é superusuário
    sql = "SELECT is_superuser FROM auth_user WHERE id = %s"
    is_superuser = executar_consulta(sql, [user_id])[0][0]

    if not is_superuser:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')

    # Lógica da página administrativa
    return render(request, 'admin_view.html')



# Logout
def logout_view(request):
    request.session.flush()  # Limpa a sessão do usuário
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')
