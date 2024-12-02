# clients/views.py
from django.shortcuts import render
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
        client_cnpj = request.POST.get('entry_client_cnpj')
        client_adress = request.POST.get('entry_client_adress')
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