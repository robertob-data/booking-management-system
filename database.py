import sqlite3

def conectar():
    conexao = sqlite3.connect('agenda.db')
    conexao.execute('PRAGMA foreign_keys = ON')
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS profissionais(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       especialidade TEXT NOT NULL,
                       telefone TEXT NOT NULL,
                       status INTEGER NOT NULL DEFAULT 1
                   )
                   
                   
                   ''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS atendimentos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_cliente TEXT NOT NULL,
                        idade_cliente INTEGER NOT NULL,
                        data_hora_marcacao TEXT NOT NULL,
                        data_hora_consulta TEXT NOT NULL,
                        procedimento TEXT NOT NULL,
                        profissional_id INTEGER NOT NULL,
                        status INTEGER NOT NULL DEFAULT 1,
                        FOREIGN KEY (profissional_id) REFERENCES profissionais (id)
                   )
                   
                   ''')
    
    conexao.commit()
    conexao.close()
    
criar_tabela()