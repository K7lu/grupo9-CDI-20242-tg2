import MySQLdb
from django.db import connection
from django.core.management.base import BaseCommand

# SQL para criar tabelas e banco de dados
CREATE_DATABASE_AND_TABLES = """
CREATE DATABASE IF NOT EXISTS sger_db;
USE sger_db;

-- Tabela Cliente
CREATE TABLE IF NOT EXISTS Cliente (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CNPJ CHAR(14) UNIQUE NOT NULL,
    Endereco VARCHAR(255),
    Telefone VARCHAR(20)
);

-- Tabela Projeto
CREATE TABLE IF NOT EXISTS Projeto (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT,
    Data_Inicio DATE,
    Data_Termino DATE,
    Cliente_ID INT NOT NULL,
    FOREIGN KEY (Cliente_ID) REFERENCES Cliente(ID)
);

-- Tabela Recurso
CREATE TABLE IF NOT EXISTS Recurso (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Tipo VARCHAR(50) NOT NULL
);

-- Tabela Alocacao_Recursos
CREATE TABLE IF NOT EXISTS Alocacao_Recursos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Recurso_ID INT NOT NULL,
    Projeto_ID INT NOT NULL,
    Quantidade INT NOT NULL,
    FOREIGN KEY (Recurso_ID) REFERENCES Recurso(ID),
    FOREIGN KEY (Projeto_ID) REFERENCES Projeto(ID)
);

-- Tabela Tarefa
CREATE TABLE IF NOT EXISTS Tarefa (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Descricao TEXT NOT NULL,
    Data_Inicio DATE,
    Data_Termino DATE,
    Status VARCHAR(20),
    Projeto_ID INT NOT NULL,
    FOREIGN KEY (Projeto_ID) REFERENCES Projeto(ID)
);

-- Tabela Funcionario
CREATE TABLE IF NOT EXISTS Funcionario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CPF CHAR(11) UNIQUE NOT NULL,
    Data_Contratacao DATE,
    Telefone VARCHAR(20)
);

-- Tabela Efetivo
CREATE TABLE IF NOT EXISTS Efetivo (
    ID INT PRIMARY KEY,
    Salario DECIMAL(10, 2) NOT NULL,
    Beneficios TEXT,
    FOREIGN KEY (ID) REFERENCES Funcionario(ID)
);

-- Tabela Terceirizado
CREATE TABLE IF NOT EXISTS Terceirizado (
    ID INT PRIMARY KEY,
    Empresa VARCHAR(100) NOT NULL,
    Valor_Hora DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID) REFERENCES Funcionario(ID)
);

-- Tabela Alocacao
CREATE TABLE IF NOT EXISTS Alocacao (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Funcionario_ID INT NOT NULL,
    Projeto_ID INT NOT NULL,
    Data_Inicio DATE NOT NULL,
    Data_Termino DATE,
    FOREIGN KEY (Funcionario_ID) REFERENCES Funcionario(ID),
    FOREIGN KEY (Projeto_ID) REFERENCES Projeto(ID)
);

-- Tabela Departamento
CREATE TABLE IF NOT EXISTS Departamento (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Responsavel_ID INT,
    FOREIGN KEY (Responsavel_ID) REFERENCES Funcionario(ID)
);

-- Tabela Cliente_Contato
CREATE TABLE IF NOT EXISTS Cliente_Contato (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Cargo VARCHAR(50),
    Email VARCHAR(150),
    Telefone VARCHAR(20),
    Cliente_ID INT NOT NULL,
    FOREIGN KEY (Cliente_ID) REFERENCES Cliente(ID)
);

CREATE TABLE IF NOT EXISTS UserRoles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
"""

def create_database_if_not_exists():
    """
    Cria o banco de dados 'sger_db' se ele não existir.
    """
    db_connection = MySQLdb.connect(
        host='localhost',
        user='admin',       # Substitua por seu usuário
        passwd='admin'      # Substitua por sua senha
    )
    cursor = db_connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS sger_db;")
    db_connection.close()

def initialize_database():
    """
    Cria as tabelas no banco de dados 'sger_db'.
    """
    with connection.cursor() as cursor:
        for statement in CREATE_DATABASE_AND_TABLES.split(";"):
            if statement.strip():
                cursor.execute(statement.strip())

class Command(BaseCommand):
    help = "Inicializa o banco de dados e cria tabelas se necessário."

    def handle(self, *args, **options):
        try:
            self.stdout.write("Criando banco de dados (se necessário)...")
            create_database_if_not_exists()

            self.stdout.write("Conectando ao banco de dados e criando tabelas...")
            initialize_database()

            self.stdout.write(self.style.SUCCESS("Banco de dados e tabelas configurados com sucesso."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao inicializar o banco de dados: {e}"))
