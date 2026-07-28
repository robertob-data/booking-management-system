from profissionais import listar_pro, cadastrar_pro, deletar_pro, atualizar_pro
from atendimento import gerar_atendimento, listar_todos_atendimentos, cancelar_atendimento, listar_atendimentos_cancelados, listar_atendimentos_concluidos, concluir_atendimento, verificar_horario
from dashboard import grafico_status, grafico_por_profissional, grafico_por_periodo
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Sistema de Agendamentos", page_icon="📅", layout="wide")
st.title('Sistema de Agendamentos')

ativos = len(listar_todos_atendimentos())
cancelados = len(listar_atendimentos_cancelados())
concluidos = len(listar_atendimentos_concluidos())
profissionais_ativos = len(listar_pro())

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Atendimentos Ativos", ativos)

with col2:
    with st.container(border=True):
        st.metric("Cancelados", cancelados)

with col3:
    with st.container(border=True):
        st.metric("Concluídos", concluidos)

with col4:
    with st.container(border=True):
        st.metric("Profissionais", profissionais_ativos)

st.divider()

with st.sidebar:
    menu = option_menu(
        menu_title="Menu",
        options=["Cadastrar Atendimento", "Atendimentos Ativos", "Cancelar Atendimento", "Concluir Atendimento", "Atendimentos Cancelados", "Atendimentos Concluídos", "Profissionais", "Dashboard"],
        icons=["calendar-plus", "list-check", "x-circle", "check-circle", "trash", "check2-all", "people", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#0e1117"},
            "icon": {"color": "#4ade80", "font-size": "18px"},
            "nav-link": {"color": "#fafafa", "font-size": "15px"},
            "nav-link-selected": {"background-color": "#1e4620", "color": "#4ade80"},
        }
    )

#Cadastrar atendimentos

if menu == 'Cadastrar Atendimento':
    st.header('Cadastrar Atendimento')

    with st.form('Formulario do Atendimento', clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            nome = st.text_input('Nome do Cliente')
        with col_b:
            idade = st.number_input('Idade do cliente', min_value=0, max_value=120, step=1, value=0)

        col_c, col_d, col_e = st.columns(3)
        with col_c:
            procedimento = st.text_input('Digite o Procedimento')
        with col_d:
            data_consulta = st.date_input('Digite o Dia do Procedimento')
        with col_e:
            hora_consulta = st.time_input('Digite a Hora do Procedimento')

        dh_consulta = datetime.combine(data_consulta, hora_consulta)

        profissionais_dict = {}
        for pro in listar_pro():
            profissionais_dict[pro[1]] = pro[0]

        if profissionais_dict:
            profissional = st.selectbox('Profissional Responsavel', profissionais_dict)
            profissional_id = profissionais_dict[profissional]
        else:
            st.warning('Nenhum profissional cadastrado')
            profissional_id = None

        if st.form_submit_button('Cadastrar Consulta'):
            if not nome or not idade or not procedimento or not dh_consulta or not profissional_id:
                st.warning('Todos os Campos devem Estar Preenchidos')
            else:
                resultado = verificar_horario(profissional_id, dh_consulta)
                if resultado:
                    st.warning('Ja Existe uma Consulta Neste Horario')
                else:
                    dh_marcacao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    gerar_atendimento(nome, idade, dh_marcacao, dh_consulta, procedimento, profissional_id)
                    st.info('Consulta Cadastrada com Sucesso')
            
            
            
        
#Listar Atendimentos
if menu == 'Atendimentos Ativos':
    st.header('Atendimentos Ativos')

    atendimentos = listar_todos_atendimentos()

    if atendimentos:
        html = """
        <style>
        .tabela-custom { width: 100%; border-collapse: collapse; }
        .tabela-custom th, .tabela-custom td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #333; }
        .badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.85em; }
        .badge-ativo { background-color: #1e4620; color: #4ade80; }
        </style>
        <table class="tabela-custom">
        <tr><th>Profissional</th><th>Cliente</th><th>Data/hora da Consulta</th><th>Procedimento</th><th>Status</th></tr>
        """
        for id, pro, nome, dh, procedi, dh_marc in atendimentos:
            html += f"<tr><td>{pro}</td><td>{nome}</td><td>{dh}</td><td>{procedi}</td><td><span class='badge badge-ativo'>Ativo</span></td></tr>"
        html += "</table>"

        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info('Nenhum Atendimento Ativo')

#cancelar atendimentos
if menu == 'Cancelar Atendimento':
    st.header('Cancelar Atendimento')

    atendimentos = listar_todos_atendimentos()
    cancelados = {}
        
    for id, pro, nome, dh, procedi, hr in atendimentos:
        cancelados[f'{nome} - {dh} - {procedi}'] = id
        
    if cancelados:    
        retorno = st.selectbox('Escolha o Atendimento a Cancelar: ', cancelados)
        atendimento_id = cancelados[retorno]
            
        if st.button('Comfirmar Cancelamento Da Consulta'):
            cancelar_atendimento(atendimento_id)
            st.info('Consulta Cancelada')
    else:
        st.info('Nenhum Atendimento Ativo')
                
 #atendimentos Cancelado           
if menu == 'Atendimentos Cancelados':
    st.header('Atendimentos Cancelados')

    atendimentos = listar_atendimentos_cancelados()

    if atendimentos:
        html = """
        <style>
        .tabela-custom { width: 100%; border-collapse: collapse; }
        .tabela-custom th, .tabela-custom td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #333; }
        .badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.85em; }
        .badge-cancelado { background-color: #4c1d1d; color: #f87171; }
        </style>
        <table class="tabela-custom">
        <tr><th>Profissional</th><th>Cliente</th><th>Data/hora da Consulta</th><th>Procedimento</th><th>Status</th></tr>
        """
        for pro, nome, dh, procedi in atendimentos:
            html += f"<tr><td>{pro}</td><td>{nome}</td><td>{dh}</td><td>{procedi}</td><td><span class='badge badge-cancelado'>Cancelado</span></td></tr>"
        html += "</table>"

        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info('Nenhum Atendimento Cancelado')
    
#menu e submenu profissionais
if menu == 'Profissionais':
    st.header('Menu dos Profissionais')
    submenu = st.radio('Menu', ['Cadastrar Profissional', 'Deletar Profissional', 'Atualizar Informaçoes', 'Profissionais Ativos'])
    
    
    if submenu == 'Cadastrar Profissional':#nome, especialidade,  telefone, status=1
        st.header('Cadastrar Profissional')
        
        with st.form('Formulario Profissional', clear_on_submit=True):
            nome = st.text_input('Nome do Profissional')
            esp = st.text_input('Especialidade')
            tel = st.text_input('Telefone (ex: 87991526893)')

            if st.form_submit_button('Cadastrar Profissional'):
                if not nome or not esp or not tel:
                    st.warning('Todos os Campos devem Estar Preenchidos')
                else:
                    cadastrar_pro(nome, esp, tel, status=1)
                    st.info('Profissional Cadastrado')
                
    
    
    if submenu == 'Deletar Profissional':
        st.header('Deletar Profissional')
        
        funcionarios = listar_pro()
        pros = {}
        for id, nome, especialidade, telefone, status in funcionarios:
            pros[f'{nome} - {especialidade}'] = id
        
        if pros:
            retorno = st.selectbox('Escolha o Profissional a Desativar', pros)
            profissional_id = pros[retorno]
            
            if st.button('[ATENÇAO] Desativar Profissional'):
                deletar_pro(profissional_id)
        else:
            st.info('Nenhum Profissional Ativo')
        
        
    if submenu == 'Atualizar Informaçoes': #id_profissional, nome, especialidade, telefone
        st.header('Atualizar Informaçoes do Profissional')
        
        funcionarios = listar_pro()
        pros = {}
        for id, nome, especialidade, telefone, status in funcionarios:
            pros[f'{nome} - {especialidade}'] = id
            
        
        if pros:
            with st.form('Formulario Atualizar Profissional', clear_on_submit=True):
                retorno = st.selectbox('Escolha o Profissional a Atualizar os Dados', pros)
                profissional_id = pros[retorno]
                nome = st.text_input('Nome do Profissional')
                esp = st.text_input('Especialidade')
                tel = st.text_input('Telefone (ex: 87991526893)')

                if st.form_submit_button('Atualizar Informaçoes'):
                    atualizar_pro(profissional_id, nome, esp, tel)
        else:
            st.info('Nenhum Profissional Ativo')
    
    
    if submenu == 'Profissionais Ativos':
        st.header('Profissionais Ativos')
        
        pros = listar_pro()
        if pros:
            dados = pd.DataFrame(pros, columns=['ID', 'Nome', 'Especialidade', 'Telefone', 'Status'])
            dados_exibir = dados.drop(columns=['ID'])
        
            dados_exibir['Status'] = dados['Status'].replace({1: 'Ativo', 0: 'Inativo'})
            
            st.table(dados_exibir)
        else:
            st.info('Nenhum Profissional Ativo')
            
            
if menu == 'Concluir Atendimento':
    st.header('Concluir Atendimento')

    atendimentos = listar_todos_atendimentos()
    concluir_dict = {}

    for id, pro, nome, dh, procedi, dh_marc in atendimentos:
        concluir_dict[f'{nome} - {dh} - {procedi}'] = (id, dh)

    if concluir_dict:
        retorno = st.selectbox('Escolha o Atendimento a Concluir: ', concluir_dict)
        atendimento_id, dh_agendado = concluir_dict[retorno]
        dh_agendado_obj = datetime.strptime(dh_agendado, "%Y-%m-%d %H:%M:%S")

        if st.button('Confirmar Conclusão'):
            
            if dh_agendado_obj < datetime.now():
                concluir_atendimento(atendimento_id)
                st.info('Atendimento marcado como concluído')
            else:
                st.warning('Nao Pode Comfirmar um Atendimento Futuro')
    else:
        st.info('Nenhum Atendimento Ativo')
        
        
if menu == 'Atendimentos Concluídos':
    st.header('Atendimentos Concluídos')

    atendimentos = listar_atendimentos_concluidos()

    if atendimentos:
        html = """
        <style>
        .tabela-custom { width: 100%; border-collapse: collapse; }
        .tabela-custom th, .tabela-custom td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #333; }
        .badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.85em; }
        .badge-concluido { background-color: #1e3a5f; color: #60a5fa; }
        </style>
        <table class="tabela-custom">
        <tr><th>Profissional</th><th>Cliente</th><th>Data/hora da Consulta</th><th>Procedimento</th><th>Status</th></tr>
        """
        for pro, nome, dh, procedi in atendimentos:
            html += f"<tr><td>{pro}</td><td>{nome}</td><td>{dh}</td><td>{procedi}</td><td><span class='badge badge-concluido'>Concluído</span></td></tr>"
        html += "</table>"

        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info('Nenhum Atendimento Concluído')          
        
    
if menu == 'Dashboard':
    st.header('Dashboard')

    col1, col2 = st.columns(2)

    with col1:
        fig1 = grafico_status()
        if fig1:
            st.pyplot(fig1)
        else:
            st.info('Nenhum atendimento cadastrado ainda')

    with col2:
        fig2 = grafico_por_profissional()
        if fig2:
            st.pyplot(fig2)
        else:
            st.info('Nenhum atendimento cadastrado ainda')

    st.divider()

    fig3 = grafico_por_periodo()
    if fig3:
        st.pyplot(fig3)
    else:
        st.info('Nenhum atendimento cadastrado ainda')