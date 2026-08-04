from database import conectar

def gerar_atendimento(nome, idade, dh_marcacao, dh_consulta, procedimento, profissional_id):
    '''
    nome: nome do cliente
    idade: idade do cliente
    dh_marcacao: data/hora em que o atendimento foi marcado (registro histórico)
    dh_consulta: data/hora em que o atendimento vai de fato acontecer
    procedimento: descrição do serviço a ser realizado
    profissional_id: id do profissional que vai atender

    Insere um novo atendimento no banco, com status ativo (1) por padrão.

    Retorna: nada (None) — apenas salva no banco
    '''
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
                   INSERT INTO atendimentos (nome_cliente, idade_cliente, data_hora_marcacao, data_hora_consulta, procedimento, profissional_id)
                   VALUES (?,?,?,?,?,?)
                   ''', (nome, idade, dh_marcacao, dh_consulta, procedimento, profissional_id))
    conexao.commit()
    conexao.close()
    

def cancelar_atendimento(id_atendimento):
    '''
    id_atendimento: id do atendimento a ser cancelado

    Faz soft delete: muda o status do atendimento para 0 (cancelado),
    sem apagar o registro do banco.

    Retorna: True se a operação foi executada
    '''
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
    '''
    id_atendimento: id do atendimento a ser removido

    ⚠️ Hard delete — apaga o registro permanentemente do banco, sem volta.
    Diferente de cancelar_atendimento (soft delete). Usar com cuidado.

    Retorna: True se a operação foi executada
    '''
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
    '''
    Busca todos os atendimentos com status 1 (ativos), já cruzando
    com a tabela profissionais para trazer o nome do profissional.

    Retorna: lista de tuplas (id, nome_profissional, nome_cliente,
    data_hora_consulta, procedimento, data_hora_marcacao)
    '''
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
    '''
    Busca todos os atendimentos com status 0 (cancelados), já cruzando
    com a tabela profissionais para trazer o nome do profissional.

    Retorna: lista de tuplas (nome_profissional, nome_cliente,
    data_hora_consulta, procedimento)
    '''
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
    '''
    Busca todos os atendimentos com status 2 (concluídos), já cruzando
    com a tabela profissionais para trazer o nome do profissional.

    Retorna: lista de tuplas (nome_profissional, nome_cliente,
    data_hora_consulta, procedimento)
    '''
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
    '''
    id_profissional: id do profissional cujos atendimentos serão buscados

    Busca todos os atendimentos vinculados a um profissional específico,
    sem filtrar por status.

    Retorna: lista de tuplas com todos os campos de atendimentos
    '''
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
    '''
    id_atendimento: id do atendimento buscado

    Busca um único atendimento pelo seu id.

    Retorna: uma tupla com todos os campos do atendimento, ou None se não existir
    '''
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
    '''
    id_atendimento: id do atendimento a ser marcado como concluído

    Atualiza o status do atendimento para 2 (concluído).

    Retorna: True se a operação foi executada
    '''

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
    '''
    profissional_id: id do profissional na tabela atendimentos
    dh_consulta: valor que vem na hora de marcar de fato
    
    a funçao realiza uma comparaçao de valores com um intervalo de 60 minutos
    caso o horario desejado esteja sobreponto este intervalo retorna o valor
    caso o horario esteja livre retorna none
    '''
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