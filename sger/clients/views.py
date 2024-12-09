# clients/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def home(request):
    return render(request, 'clients/home.html')

def clients_list(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Salva o registro do cliente
    if request.method == 'POST':
        client_name = request.POST.get('entry_client_name')
        client_cnpj = request.POST.get('clean_cnpj')
        client_adress = request.POST.get('entry_client_address')
        client_phone = request.POST.get('entry_client_phone')


        # Insere o novo cliente na tabela
        sql_insert = """
        INSERT INTO Cliente (Nome, CNPJ, Endereco, Telefone)
        VALUES (%s, %s, %s, %s)
        """
        executar_consulta(sql_insert, [client_name, client_cnpj, client_adress, client_phone])

    # Busca todos os clientes para exibir na página
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente ORDER BY Nome"
    clients = executar_consulta(sql_select)  # Definição da variável 'clients'

    # Passa os dados para o template
    context = {
        'clients': clients  # 'clients' contém os dados retornados pela consulta SQL
    }
    return render(request, 'clients/clients_list.html', context)


def clients_register_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os clientes
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente ORDER BY Nome"
    clients = executar_consulta(sql_select)

    context = {
        'clients': clients  # 'clients' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de clientes
    return render(request, 'clients/clients_register.html', {'clientsList': context})

def clients_search_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Pega o termo de pesquisa (caso exista)
    search_term = request.GET.get('search_term', '').strip()

    # Consulta para buscar todos os clientes, ou aplicar filtro de pesquisa se necessário
    sql_select = """
        SELECT ID, Nome, CNPJ, Endereco, Telefone 
        FROM Cliente
        WHERE Nome LIKE %s OR CNPJ LIKE %s OR Endereco LIKE %s OR Telefone LIKE %s
        ORDER BY Nome
    """

    # Parametros de pesquisa
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']

    clients = executar_consulta(sql_select, parametros)

    # Passa os dados para o template
    context = {
        'clients': clients,  # Lista de clientes
    }
    return render(request, 'clients/clients_list.html', context)

def delete_clients_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para verificar se o cliente existe
    sql_select = "SELECT ID FROM Cliente WHERE ID = %s"
    client_exists = executar_consulta(sql_select, [id])

    # Se o cliente não existir, redireciona com uma mensagem de erro
    if not client_exists:
        messages.error(request, "Cliente não encontrado!")
        return redirect('clients_list')

    # Consulta SQL para deletar o cliente
    sql_delete = "DELETE FROM Cliente WHERE ID = %s"
    executar_consulta(sql_delete, [id])

    # Mensagem de sucesso
    messages.info(request, 'Cliente deletado com sucesso!')
    return redirect('clients_list')

def edit_client_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para buscar os dados do cliente
    sql_select = "SELECT ID, Nome, CNPJ, Endereco, Telefone FROM Cliente WHERE ID = %s"
    client_data = executar_consulta(sql_select, [id])

    if not client_data:
        messages.error(request, "Cliente não encontrado!")
        return redirect('clients_list')

    # Se o método da requisição for POST, atualiza os dados
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
        messages.add_message(request, messages.INFO, 'Cliente atualizado com sucesso!')
        return redirect('clients_list')

    # Caso seja um GET, exibe o modal com os dados atuais
    client = client_data[0]  # Extraindo os dados do cliente da lista
    context = {
        'client': client
    }
    return render(request, 'clients/clients_list.html', context)