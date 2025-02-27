from flask import g
import sqlite3

def conectar_db():
    """
    Estabelece uma conexão com o banco de dados SQLite.
    Configura a fábrica de linhas para retornar dicionários ao invés de tuplas.
    """
    sql = sqlite3.connect('alunos.db')
    sql.row_factory = sqlite3.Row # Retorna as consultas como dicionários ao invés de tuplas
    return sql

def get_db():
    """
    Obtém a conexão com o banco de dados armazenada em g.
    Se não existir, cria uma nova conexão e a armazena em g.
    """
    if not hasattr(g, 'sqlite_db'): # Verifica se 'sqlite_db' NÃO existe em 'g'
        g.sqlite_db = conectar_db() # Cria a conexão com o banco de dados e armazena essa conexão em 'g'
    return g.sqlite_db
