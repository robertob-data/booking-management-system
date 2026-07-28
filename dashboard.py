from atendimento import listar_atendimentos_cancelados, listar_todos_atendimentos, listar_atendimentos_concluidos
import matplotlib.pyplot as plt

plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#0e1117'
plt.rcParams['text.color'] = '#fafafa'
plt.rcParams['axes.labelcolor'] = '#fafafa'
plt.rcParams['xtick.color'] = '#fafafa'
plt.rcParams['ytick.color'] = '#fafafa'

def contar_status():
    ativos = len(listar_todos_atendimentos())
    cancelados = len(listar_atendimentos_cancelados())
    concluidos = len(listar_atendimentos_concluidos())
    return (ativos, cancelados, concluidos)

def grafico_status():
    ativos, cancelados, concluidos = contar_status()
    dados = {'Ativos': (ativos, '#4ade80'), 'Cancelados': (cancelados, '#f87171'), 'Concluídos': (concluidos, '#60a5fa')}
    
    dados_filtrados = {k: v for k, v in dados.items() if v[0] > 0}
    
    if not dados_filtrados:
        return None
    
    rotulos = [f'{nome}: {valor}' for nome, (valor, cor) in dados_filtrados.items()]
    valores = [valor for valor, cor in dados_filtrados.values()]
    cores = [cor for valor, cor in dados_filtrados.values()]
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(valores, labels=rotulos, colors=cores, autopct='%1.0f%%',
           wedgeprops={'edgecolor': '#0e1117', 'linewidth': 2},
           textprops={'fontsize': 9})
    ax.set_title('Atendimentos por Status', fontsize=13, fontweight='bold', pad=10)
    fig.tight_layout()
    return fig

def contar_por_profissional():
    atendimentos = listar_todos_atendimentos()
    contagem = {}
    for id, pro, nome, dh, procedi, dh_marc in atendimentos:
        if pro in contagem:
            contagem[pro] += 1
        else:
            contagem[pro] = 1
    return contagem

def grafico_por_profissional():
    contagem = contar_por_profissional()

    if not contagem:
        return None

    profissionais = list(contagem.keys())
    quantidades = list(contagem.values())

    fig, ax = plt.subplots(figsize=(4, 4))
    barras = ax.bar(profissionais, quantidades, color='#4ade80', edgecolor='#0e1117', width=0.5)
    ax.set_title('Atendimentos por Profissional', fontsize=13, fontweight='bold', pad=10)
    ax.set_ylabel('Quantidade')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.setp(ax.get_xticklabels(), rotation=20, ha='right', fontsize=8)

    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, altura + 0.05, int(altura),
                ha='center', fontsize=10, fontweight='bold')

    fig.tight_layout()
    return fig

def contar_por_dia():
    todos = listar_todos_atendimentos() + [(*a, None, None) for a in listar_atendimentos_cancelados()] + [(*a, None, None) for a in listar_atendimentos_concluidos()]

    contagem = {}
    for atendimento in todos:
        dh = atendimento[3] if len(atendimento) > 4 else atendimento[2]
        dia = dh.split(' ')[0]
        contagem[dia] = contagem.get(dia, 0) + 1

    dias_ordenados = sorted(contagem.keys())
    valores_ordenados = [contagem[dia] for dia in dias_ordenados]
    return dias_ordenados, valores_ordenados

def grafico_por_periodo():
    dias, valores = contar_por_dia()

    if not dias:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dias, valores, marker='o', color='#4ade80', linewidth=2, markersize=6)
    ax.fill_between(dias, valores, alpha=0.15, color='#4ade80')
    ax.set_title('Atendimentos por Período', fontsize=13, fontweight='bold', pad=10)
    ax.set_ylabel('Quantidade')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    return fig