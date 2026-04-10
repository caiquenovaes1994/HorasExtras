import streamlit as st
import pandas as pd
from datetime import datetime, time
import database
import utils
import report_generator
import os

# Configuração da Página
st.set_page_config(page_title="Controle de Horas Extras", layout="wide")

# Inicializar Banco de Dados
database.init_db()

# Estilo Customizado (Cores e Fontes)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #800000;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #a00000;
        color: white;
    }
    .header-style {
        color: #800000;
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #800000;
        margin-bottom: 30px;
        font-weight: bold;
    }
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Gerenciamento de Sessão de Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# 1. TELA DE LOGIN
if not st.session_state.logged_in:
    st.markdown("<h1 class='header-style'>ACESSO AO SISTEMA</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("ENTRAR")
            
            if submit_login:
                user = database.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
    st.stop()

# 2. TELA DE TROCA DE SENHA OBRIGATÓRIA
if st.session_state.user.get('precisa_trocar_senha'):
    st.markdown("<h1 class='header-style'>TROCA DE SENHA OBRIGATÓRIA</h1>", unsafe_allow_html=True)
    st.warning("Para sua segurança, você deve alterar sua senha no primeiro acesso.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("change_password_form"):
            new_password = st.text_input("Nova Senha", type="password")
            confirm_password = st.text_input("Confirme a Nova Senha", type="password")
            submit_pass = st.form_submit_button("ALTERAR SENHA")
            
            if submit_pass:
                if len(new_password) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                elif new_password != confirm_password:
                    st.error("As senhas não coincidem.")
                else:
                    database.update_password(st.session_state.user['id'], new_password)
                    st.session_state.user['precisa_trocar_senha'] = False
                    st.success("Senha alterada com sucesso!")
                    st.rerun()
    st.stop()

# 3. CONTEÚDO PRINCIPAL (APP)
st.markdown("<h1 class='header-style'>CONTROLE DE HORAS EXTRAS</h1>", unsafe_allow_html=True)

# Sidebar para Filtros e Configurações
with st.sidebar:
    st.header(f"👤 Bem-vindo, {st.session_state.user['nome_completo']}")
    if st.button("Sair"):
        logout()
    
    st.markdown("---")
    st.header("📅 Relatório PDF")
    meses_pt = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    mes_ref = st.selectbox("Mês Referente", meses_pt, index=datetime.now().month - 1)
    ano_ref = st.number_input("Ano", min_value=2024, max_value=2030, value=datetime.now().year)
    
    if st.button("🚀 GERAR RELATÓRIO PDF"):
        rows = database.get_all_chamados()
        if not rows:
            st.error("Nenhum dado encontrado.")
        else:
            df_full = pd.DataFrame(rows, columns=['id', 'data', 'caso', 'pms', 'hotel', 'inicio', 'termino', 'observacoes'])
            df_agrupado = utils.agrupar_por_data(df_full)
            pdf_file = f"Folha_Horas_{mes_ref}_{ano_ref}.pdf"
            report_generator.gerar_pdf(df_agrupado, st.session_state.user['nome_completo'], mes_ref, str(ano_ref), pdf_file)
            
            with open(pdf_file, "rb") as f:
                st.download_button(label="📂 Baixar PDF Gerado", data=f, file_name=pdf_file, mime="application/pdf")
            st.success("PDF gerado!")

# Tabs do Sistema
menu_items = ["📝 Novo Registro", "📋 Histórico"]
if st.session_state.user['is_admin']:
    menu_items.append("⚙️ Gestão de Usuários")

tabs = st.tabs(menu_items)

with tabs[0]:
    st.subheader("Inserir Novo Chamado")
    hoteis_db = database.get_hoteis()
    hotel_options = [f"{rid} - {nome}" for rid, nome in hoteis_db] if hoteis_db else ["Nenhum hotel encontrado"]
    
    with st.form("form_chamado", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            f_data = st.date_input("Data do Atendimento", value=datetime.now())
            f_caso = st.text_input("Caso / INC", placeholder="Ex: INC123456")
        with col2:
            f_hotel_sel = st.selectbox("Hotel / PMS", options=hotel_options)
            # Extrair RID e Nome
            if " - " in f_hotel_sel:
                f_pms, f_hotel = f_hotel_sel.split(" - ", 1)
            else:
                f_pms, f_hotel = "", f_hotel_sel
        with col3:
            f_inicio = st.time_input("Horário Início", value=time(8, 0))
            f_termino = st.time_input("Horário Término", value=time(9, 0))
        
        f_obs = st.text_area("Observações", placeholder="Detalhes do atendimento...")
        submitted = st.form_submit_button("Salvar Chamado")
        
        if submitted:
            if not f_caso:
                st.error("O campo 'Caso / INC' é obrigatório.")
            else:
                database.save_chamado(f_data.strftime('%Y-%m-%d'), f_caso, f_pms, f_hotel, f_inicio.strftime('%H:%M'), f_termino.strftime('%H:%M'), f_obs)
                st.success("Chamado registrado!")
                st.rerun()

with tabs[1]:
    st.subheader("Histórico de Chamados")
    rows = database.get_all_chamados()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'Data', 'Caso/INC', 'PMS', 'Hotel', 'Início', 'Término', 'Observações'])
        df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
        st.dataframe(df.drop(columns=['ID']), use_container_width=True)
        
        with st.expander("🗑️ Deletar Registro"):
            id_a_deletar = st.number_input("ID para deletar", min_value=1, step=1)
            if st.button("Confirmar Exclusão"):
                database.delete_chamado(id_a_deletar)
                st.warning(f"Registro {id_a_deletar} removido.")
                st.rerun()
    else:
        st.info("Nenhum chamado registrado.")

if st.session_state.user['is_admin']:
    with tabs[2]:
        st.subheader("Gestão de Usuários")
        
        with st.expander("➕ Criar Novo Usuário"):
            with st.form("new_user_form"):
                new_user = st.text_input("Username")
                new_pass = st.text_input("Senha Inicial", type="password")
                new_name = st.text_input("Nome Completo")
                new_admin = st.checkbox("Administrador")
                if st.form_submit_button("CRIAR USUÁRIO"):
                    if database.create_user(new_user, new_pass, new_name, new_admin):
                        st.success("Usuário criado!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar usuário (Username já existe).")
        
        users = database.get_all_users()
        df_users = pd.DataFrame(users, columns=['ID', 'Username', 'Nome', 'Admin', 'Trocar Senha'])
        st.dataframe(df_users, use_container_width=True)
        
        with st.expander("🗑️ Deletar Usuário"):
            user_id_del = st.number_input("ID do Usuário para deletar", min_value=1, step=1)
            if st.button("Confirmar Exclusão de Usuário"):
                if user_id_del == st.session_state.user['id']:
                    st.error("Você não pode deletar a si mesmo.")
                else:
                    database.delete_user(user_id_del)
                    st.success(f"Usuário {user_id_del} removido.")
                    st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Desenvolvido para Caique Novaes - Automação de Horas Extras</p>", unsafe_allow_html=True)
