from django.db import connection

def executar_consulta(sql, parametros=None):
    """
    Executa consultas SQL diretamente no banco de dados.
    Retorna os resultados para SELECT, ou None para outras operações.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, parametros or [])
        if sql.strip().lower().startswith("select"):
            return cursor.fetchall()  # Retorna resultados para SELECT
        return None  # Para INSERT, UPDATE, DELETE
