from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


def department_register_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Salva o registro do departamento
    if request.method == 'POST':
        department_name = request.POST.get('entry_department_name')
        responsible_employee_id = request.POST.get('entry_responsible_employee')

        # Insere o novo departamento na tabela
        sql_insert = """
        INSERT INTO Departamento (Nome, Responsavel_ID)
        VALUES (%s, %s)
        """
        executar_consulta(sql_insert, [department_name, responsible_employee_id])

        return redirect('departments_list')

    # Busca todos os departamentos para exibição na tabela
    sql_select_departments = """
        SELECT ID, Nome, Responsavel_ID
        FROM Departamento
        ORDER BY Nome
    """
    departments = executar_consulta(sql_select_departments)

    # Busca todos os funcionários para preencher o campo de seleção no formulário
    sql_select_employees = "SELECT ID, Nome FROM Funcionario ORDER BY Nome"
    employees = executar_consulta(sql_select_employees)

    # Passa os dados para o template
    context = {
        'departments': departments,  # Dados dos departamentos
        'employees': employees       # Lista de funcionários para o formulário
    }
    return render(request, 'departments/department_register.html', context)

def department_list_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Consulta para buscar todos os departamentos
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
    departments = executar_consulta(sql_select)

    context = {
        'departments': departments  # 'departments' contém os dados retornados pela consulta SQL
    }
    # Renderiza o template com a lista de departamentos
    return render(request, 'departments/department_list.html', context)


def departments_search_view(request):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Obtém o termo de pesquisa
    search_term = request.GET.get('search_term', '').strip()

    # Consulta SQL para buscar departamentos pelo termo
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
    departments = executar_consulta(sql_select, parametros)

    context = {
        'departments': departments,
    }
    return render(request, 'departments/department_list.html', context)


def delete_department_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

    # Verifica se o departamento existe
    sql_select = "SELECT ID FROM Departamento WHERE ID = %s"
    department_exists = executar_consulta(sql_select, [id])

    if not department_exists:
        messages.error(request, "Departamento não encontrado!")
        return redirect('departments_list')

    # Deleta o departamento
    sql_delete = "DELETE FROM Departamento WHERE ID = %s"
    executar_consulta(sql_delete, [id])

    messages.info(request, 'Departamento deletado com sucesso!')
    return redirect('departments_list')


def edit_department_view(request, id):
    # Função auxiliar para executar consultas SQL
    def executar_consulta(sql, parametros=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros or [])
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()

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
    department_data = executar_consulta(sql_select, [id])

    if not department_data:
        messages.error(request, "Departamento não encontrado!")
        return redirect('departments_list')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        funcionario_responsavel_id = request.POST.get('responsible')

        # Atualiza os dados do departamento
        sql_update = """
        UPDATE Departamento
        SET Nome = %s, Responsavel_ID = %s
        WHERE ID = %s
        """
        executar_consulta(sql_update, [nome, funcionario_responsavel_id, id])

        messages.info(request, 'Departamento atualizado com sucesso!')
        return redirect('departments_list')

    # Pega a lista de funcionários para o dropdown
    sql_select_employees = "SELECT ID, Nome FROM Funcionario ORDER BY Nome"
    employees = executar_consulta(sql_select_employees)

    context = {
        'department': department_data[0],  # Dados do departamento
        'employees': employees,           # Lista de funcionários
    }
    return render(request, 'departments/department_edit.html', context)
