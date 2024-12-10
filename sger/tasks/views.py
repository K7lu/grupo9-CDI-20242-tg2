# tasks/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from projects.models import Project

def tasks_manager(request):
    return render(request, 'tasks/home.html')

def tasks_register(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Salva o registro do projeto
    if request.method == 'POST':
        task_description = request.POST.get('entry_task_description')
        task_start_date = request.POST.get('entry_task_start_date')
        task_end_date = request.POST.get('entry_task_end_date')
        task_status = request.POST.get('entry_task_status')
        project_name = request.POST.get('entry_task_project')

        # Insere a nova tarefa na tabela
        sql_insert = """
        INSERT INTO Tarefa (Descricao, Data_Inicio, Data_Termino, Status, Projeto_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        executar_consulta(sql_insert, [task_description, task_start_date, task_end_date, task_status, project_name])

        return redirect('tasks_list')
    
    # Busca todos os projetos para exibir na página
    sql_select = """
    SELECT  ID, Descricao, Data_Inicio, Data_Termino, Status From Tarefa ORDER BY Descricao
    """
    tasks = executar_consulta(sql_select)

    # Busca todos os projetos para preencher o campo de seleção no formulário
    sql_select_projects = "SELECT ID, Nome FROM Projeto ORDER BY Nome"
    projects = executar_consulta(sql_select_projects)

    # Passa os dados para o template
    context = {
        'tasks': tasks,  # Dados dos tarefas
        'projects': projects     # Lista de projetos para o formulário
    }
    return render(request, 'tasks/tasks_register.html', context)

def tasks_list(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os projetos
    sql_select = """
    SELECT 
        Tarefa.ID, Tarefa.Descricao, Tarefa.Data_Inicio, Tarefa.Data_Termino, Tarefa.Status, Projeto.Nome AS Projeto_Nome
    FROM 
        Tarefa
    LEFT JOIN 
        Projeto ON Tarefa.Projeto_ID = Projeto.ID
    ORDER BY 
        Projeto.Nome
    """
    tasks = executar_consulta(sql_select)    

    context = {
        'tasks': tasks  # 'projects' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de projetos
    return render(request, 'tasks/tasks_list.html', context)

def tasks_register_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os clientes
    sql_select = "SELECT ID, Descricao, Data_inicio, Data_termino, Status FROM Cliente ORDER BY Data_inicio"
    tasks = executar_consulta(sql_select)

    context = {
        'tasks': tasks  # 'clients' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de clientes
    return render(request, 'tasks/tasks_register.html', {'tasksList': context})

def tasks_search_view(request):
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
        SELECT ID, Descricao, Data_Inicio, Data_Termino
        FROM Tarefa
        WHERE Descricao LIKE %s OR Data_Inicio LIKE %s OR Data_Termino LIKE %s OR Status LIKE %s
        ORDER BY Data_Inicio
    """

    # Parâmetros de pesquisa
    parametros = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']

    tasks = executar_consulta(sql_select, parametros)

    # Passa os dados para o template
    context = {
        'tasks': tasks,  # Lista de projetos
    }
    return render(request, 'tasks/tasks_list.html', context)

def delete_tasks_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para verificar se o projeto existe
    sql_select = "SELECT ID FROM Tarefa WHERE ID = %s"
    task_exists = executar_consulta(sql_select, [id])

    # Se o projeto não existir, redireciona com uma mensagem de erro
    if not task_exists:
        messages.error(request, "Projeto não encontrado!")
        return redirect('tasks_list')

    # Consulta SQL para deletar o projeto
    sql_delete = "DELETE FROM Tarefa WHERE ID = %s"
    executar_consulta(sql_delete, [id])

    # Mensagem de sucesso
    messages.info(request, 'Tarefa deletada com sucesso!')
    return redirect('tasks_list')

def edit_task_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta SQL para buscar os dados do projeto
    sql_select = "SELECT ID, Descricao, Data_Inicio, Data_Termino, Status FROM Tarefa WHERE ID = %s"
    task_data = executar_consulta(sql_select, [id])

    if not task_data:
        messages.error(request, "Tarefa não encontrada!")
        return redirect('tasks_list')

    # Se o método da requisição for POST, atualiza os dados
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        status = request.POST.get('status')

        sql_update = """
        UPDATE Tarefa
        SET Descricao = %s, Data_Inicio = %s, Data_Termino = %s, Status = %s
        WHERE ID = %s
        """
        executar_consulta(sql_update, [descricao, data_inicio, data_termino, status, id])
        messages.add_message(request, messages.INFO, 'Tarefa atualizada com sucesso!')
        return redirect('tasks_list')

    # Caso seja um GET, exibe o modal com os dados atuais
    task = task_data[0]  # Extraindo os dados do projeto da lista
    context = {
        'task': task
    }
    return render(request, 'tasks/tasks_list.html', context)
