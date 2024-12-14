import os
import sys
import django
from django.core.management import execute_from_command_line
from initialize_database import initialize_database

# Configura o ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sger.settings")
django.setup()

if __name__ == "__main__":
    # Verifica se o comando atual é 'runserver' ou outro que dependa do banco
    if "runserver" in sys.argv or "migrate" in sys.argv or "createsuperuser" in sys.argv:
        print("Inicializando o banco de dados, se necessário...")
        try:
            initialize_database()  # Cria o banco de dados e tabelas, se não existirem
        except Exception as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
            sys.exit(1)

    # Executa o comando do Django
    execute_from_command_line(sys.argv)
