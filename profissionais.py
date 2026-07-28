from database import conectar

def cadastrar_pro(nome, especialidade,  telefone, status=1):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute(''' 
                   INSERT INTO profissionais (nome, especialidade, telefone, status)
                   VALUES (?,?,?,?)
                   ''', (nome, especialidade, telefone, status))
    conexao.commit()
    conexao.close()
    return True

def deletar_pro(id_profissional):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   UPDATE profissionais 
                   SET status = 0
                   WHERE id = ?
                   ''', (id_profissional,))
    
    conexao.commit()
    conexao.close()
    
    return True

def listar_pro():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT * FROM profissionais
                   WHERE status = 1
                   ''')
    resultado = cursor.fetchall()
    conexao.close()
    
    return resultado

def atualizar_pro(id_profissional, nome, especialidade, telefone):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   UPDATE profissionais 
                   SET nome = ?, especialidade = ?, telefone = ?
                   WHERE id = ?
                   ''', (nome, especialidade, telefone, id_profissional,))
    
    conexao.commit()
    conexao.close()
    
    return True
    
    

    