# proojects/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from clients.models import Client  

def projects_manager(request):
    return render(request, 'projects/home.html')

def projects_register(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Salva o registro do projeto
    if request.method == 'POST':
        project_name = request.POST.get('entry_project_name')
        project_description = request.POST.get('entry_project_description')
        project_start_date = request.POST.get('entry_project_start_date')
        project_end_date = request.POST.get('entry_project_end_date')
        client_name = request.POST.get('entry_project_client')

        # Insere o novo projeto na tabela
        sql_insert = """
        INSERT INTO Projeto (Nome, Descricao, Data_Inicio, Data_Termino, Cliente_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        executar_consulta(sql_insert, [project_name, project_description, project_start_date, project_end_date, client_name])

        return redirect('projects_register')
    
    # Busca todos os projetos para exibir na página
    sql_select = """
    SELECT  ID, Nome, Descricao, Data_Inicio, Data_Termino From Projeto ORDER BY Nome
    """
    projects = executar_consulta(sql_select)

    # Busca todos os clientes para preencher o campo de seleção no formulário
    sql_select_clients = "SELECT ID, Nome FROM Cliente ORDER BY Nome"
    clients = executar_consulta(sql_select_clients)

    # Passa os dados para o template
    context = {
        'projects': projects,  # Dados dos projetos
        'clients': clients     # Lista de clientes para o formulário
    }
    return render(request, 'projects/projects_register.html', context)

def projects_list(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os projetos
    sql_select = "SELECT ID, Nome, Descricao, Data_Inicio, Data_Termino FROM Projeto ORDER BY Nome"
    projects = executar_consulta(sql_select)

    context = {
        'projects': projects  # 'projects' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de projetos
    return render(request, 'projects/projects_list.html', context)

def projects_register_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os clientes
    sql_select = "SELECT ID, Nome, Descricao, Data_inicio, Data_termino FROM Cliente ORDER BY Nome"
    projects = executar_consulta(sql_select)

    context = {
        'projects': projects  # 'clients' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de clientes
    return render(request, 'porjects/projects_register.html', {'projectsList': context})

def projects_search_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Pega o termo de pesquisa (caso exista)
    search_term = request.GET.get('search_term', '').strip()

    # Consulta para buscar todos os projetos, ou aplicar filtro de pesquisa se necessário
    sql_select = """
        SELECT ID, Nome, Descricao, Data_Inicio, Data_Termino
        FROM Projeto
        WHERE Nome LIKE %s OR Descricao LIKE %s OR Data_Inicio LIKE %s OR Data_Termino LIKE %s
        ORDER BY Nome
    """

    # Parâmetros de pesquisa
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']

    projects = executar_consulta(sql_select, parametros)

    # Passa os dados para o template
    context = {
        'projects': projects,  # Lista de projetos
    }
    return render(request, 'projects/projects_list.html', context)

def delete_projects_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para verificar se o projeto existe
    sql_select = "SELECT ID FROM Projeto WHERE ID = %s"
    project_exists = executar_consulta(sql_select, [id])

    # Se o projeto não existir, redireciona com uma mensagem de erro
    if not project_exists:
        messages.error(request, "Projeto não encontrado!")
        return redirect('projects_list')

    # Consulta SQL para deletar o projeto
    sql_delete = "DELETE FROM Projeto WHERE ID = %s"
    executar_consulta(sql_delete, [id])

    # Mensagem de sucesso
    messages.info(request, 'Projeto deletado com sucesso!')
    return redirect('projects_list')

def edit_project_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para buscar os dados do projeto
    sql_select = "SELECT ID, Nome, Descricao, Data_Inicio, Data_Termino FROM Projeto WHERE ID = %s"
    project_data = executar_consulta(sql_select, [id])

    if not project_data:
        messages.error(request, "Projeto não encontrado!")
        return redirect('projects_list')

    # Se o método da requisição for POST, atualiza os dados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')

        sql_update = """
        UPDATE Projeto
        SET Nome = %s, Descricao = %s, Data_Inicio = %s, Data_Termino = %s
        WHERE ID = %s
        """
        executar_consulta(sql_update, [nome, descricao, data_inicio, data_termino, id])
        messages.add_message(request, messages.INFO, 'Projeto atualizado com sucesso!')
        return redirect('projects_list')

    # Caso seja um GET, exibe o modal com os dados atuais
    project = project_data[0]  # Extraindo os dados do projeto da lista
    context = {
        'project': project
    }
    return render(request, 'projects/projects_list.html', context)
