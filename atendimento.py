from database import conectar

def gerar_atendimento(nome, idade, dh_marcacao, dh_consulta, procedimento, profissional_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   INSERT INTO atendimentos (nome_cliente, idade_cliente, data_hora_marcacao, data_hora_consulta, procedimento, profissional_id)
                   VALUES (?,?,?,?,?,?)
                   ''', (nome, idade, dh_marcacao, dh_consulta, procedimento, profissional_id))
    conexao.commit()
    conexao.close()
    

def cancelar_atendimento(id_atendimento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   UPDATE atendimentos
                   SET status = 0
                   WHERE id = ?
                   ''', (id_atendimento,))
    
    conexao.commit()
    conexao.close()
    return True

def deletar_atendimento(id_atendimento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute(''' 
                   DELETE FROM atendimentos
                   WHERE id = ?
                   ''', (id_atendimento,))
    
    conexao.commit()
    conexao.close()
    return True



def listar_todos_atendimentos():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT atendimentos.id, profissionais.nome, atendimentos.nome_cliente, atendimentos.data_hora_consulta, atendimentos.procedimento,atendimentos.data_hora_marcacao
                   FROM atendimentos
                   JOIN profissionais ON atendimentos.profissional_id = profissionais.id
                   WHERE atendimentos.status = 1
                   ''')
    resultado = cursor.fetchall()
    conexao.close()

    return resultado

def listar_atendimentos_cancelados():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT profissionais.nome, atendimentos.nome_cliente, atendimentos.data_hora_consulta, atendimentos.procedimento
                   FROM atendimentos
                   JOIN profissionais ON atendimentos.profissional_id = profissionais.id
                   WHERE atendimentos.status = 0
                   ''')
    resultado = cursor.fetchall()
    conexao.close()
    
    return resultado
    
    
def listar_atendimentos_concluidos():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                    SELECT profissionais.nome, atendimentos.nome_cliente, atendimentos.data_hora_consulta, atendimentos.procedimento
                    FROM atendimentos
                    JOIN profissionais ON atendimentos.profissional_id = profissionais.id
                    WHERE atendimentos.status = 2                    
                    ''')
    resultado = cursor.fetchall()
    conexao.close()
    
    return resultado

def listar_atendimentos_por_profissional(id_profissional):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT * FROM atendimentos
                   WHERE profissional_id = ?
                   ''', (id_profissional,))
    
    resultado = cursor.fetchall()
    
    conexao.close()
    return resultado

def buscar_atendimento_id(id_atendimento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT * FROM atendimentos
                   WHERE id = ?
                   ''', (id_atendimento,))
    
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def concluir_atendimento(id_atendimento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   UPDATE atendimentos
                   SET status = 2
                   WHERE id = ?
                   ''', (id_atendimento,))
    
    conexao.commit()
    conexao.close()
    return True

def verificar_horario(profissional_id, dh_consulta):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   SELECT * FROM atendimentos
                   WHERE profissional_id = ?
                   AND status = 1
                   AND ABS((julianday(?) - julianday(data_hora_consulta)) * 1440) < 60
                   ''', (profissional_id, dh_consulta))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado