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

# Estilo Customizado
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #800000; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #a00000; color: white; }
    .header-style { color: #800000; text-align: center; padding-bottom: 20px; border-bottom: 2px solid #800000; margin-bottom: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- Modais (st.dialog) ---

@st.dialog("Cadastrar Novo Hotel")
def modal_novo_hotel():
    with st.form("form_novo_hotel", clear_on_submit=True):
        rid = st.text_input("Código (RID)")
        nome = st.text_input("Nome do Hotel")
        if st.form_submit_button("CADASTRAR"):
            if rid and nome:
                if database.save_hotel(rid, nome):
                    st.success("Hotel cadastrado!")
                    st.rerun()
                else: st.error("Erro: Código já existe.")

@st.dialog("Editar Hotel")
def modal_editar_hotel(rid, nome):
    with st.form("form_edit_hotel"):
        new_rid = st.text_input("Código (RID)", value=rid)
        new_nome = st.text_input("Nome do Hotel", value=nome)
        if st.form_submit_button("SALVAR ALTERAÇÕES"):
            if database.update_hotel(rid, new_rid, new_nome):
                st.success("Hotel atualizado!")
                st.rerun()
            else: st.error("Erro ao atualizar.")

@st.dialog("Cadastrar Novo Usuário")
def modal_novo_usuario():
    with st.form("form_novo_user", clear_on_submit=True):
        user = st.text_input("Usuário")
        pw = st.text_input("Senha Inicial", type="password")
        name = st.text_input("Nome Completo")
        admin = st.checkbox("Administrador")
        if st.form_submit_button("CRIAR"):
            if user and pw and name:
                if database.create_user(user, pw, name, admin):
                    st.success("Usuário criado!")
                    st.rerun()
                else: st.error("Erro: Usuário já existe.")

@st.dialog("Editar Usuário")
def modal_editar_usuario(uid, user, name, admin):
    with st.form("form_edit_user"):
        new_user = st.text_input("Usuário", value=user)
        new_name = st.text_input("Nome Completo", value=name)
        new_admin = st.checkbox("Administrador", value=admin)
        new_pw = st.text_input("Nova Senha (deixe em branco para manter)", type="password")
        if st.form_submit_button("SALVAR"):
            if database.update_user(uid, new_user, new_name, new_admin, new_pw if new_pw else None):
                st.success("Usuário atualizado!")
                st.rerun()
            else: st.error("Erro ao atualizar.")

# --- Autenticação ---

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# Validar integridade da sessão (evita KeyError: 'nome' em sessões antigas)
if st.session_state.logged_in and (not isinstance(st.session_state.user, dict) or 'nome' not in st.session_state.user):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

if not st.session_state.logged_in:
    st.markdown("<h1 class='header-style'>ACESSO AO SISTEMA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("ENTRAR"):
                user = database.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else: st.error("Credenciais inválidas.")
    st.stop()

if st.session_state.user.get('must_change'):
    st.markdown("<h1 class='header-style'>TROCA DE SENHA OBRIGATÓRIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("pw_change"):
            np = st.text_input("Nova Senha", type="password")
            cp = st.text_input("Confirme a Senha", type="password")
            if st.form_submit_button("ALTERAR"):
                if np == cp and len(np) >= 6:
                    database.update_password(st.session_state.user['id'], np)
                    st.session_state.user['must_change'] = False
                    st.rerun()
                else: st.error("Verifique os critérios.")
    st.stop()

# --- Conteúdo Principal ---

st.markdown("<h1 class='header-style'>CONTROLE DE HORAS EXTRAS</h1>", unsafe_allow_html=True)

with st.sidebar:
    nome_exibicao = st.session_state.user.get('nome', 'Usuário')
    st.header(f"👤 {nome_exibicao}")
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.header("📅 Relatório PDF")
    meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    m_sel = st.selectbox("Mês Referente", meses, index=datetime.now().month - 1)
    a_sel = st.number_input("Ano", 2024, 2030, datetime.now().year)
    if st.button("🚀 GERAR PDF"):
        rows = database.get_all_chamados()
        df = pd.DataFrame(rows, columns=['id','data','caso','pms','hotel','inicio','termino','obs'])
        df_ag = utils.agrupar_por_data(df, m_sel, a_sel)
        report_generator.gerar_pdf(df_ag, st.session_state.user['nome'], m_sel, str(a_sel))
        with open("folha_horas.pdf", "rb") as f:
            st.download_button("📂 Baixar PDF", f, "Folha_Horas.pdf", "application/pdf")

tabs = st.tabs(["📝 Novo Registro", "📋 Histórico", "🏨 Hotéis", "⚙️ Usuários"])

with tabs[0]:
    st.subheader("Inserir Novo Chamado")
    h_rows = database.get_hoteis()
    h_opts = [f"{r} - {n}" for r, n in h_rows]
    
    with st.form("novo_registro", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_data = st.date_input("Data do Atendimento", value=datetime.now())
            f_caso = st.text_input("Caso / INC (Opcional)")
        with c2:
            f_hsel = st.selectbox("Hotel / PMS", h_opts)
            f_rid, f_hnome = f_hsel.split(" - ", 1) if " - " in f_hsel else ("", f_hsel)
        with c3:
            # Máscara aplicada no processamento
            f_inicio = st.text_input("Início (ex: 0730)", value="08:00")
            f_fim = st.text_input("Término (ex: 1730)", value="17:00")
        f_obs = st.text_area("Observações")
        if st.form_submit_button("SALVAR"):
            ti = utils.processar_input_horario(f_inicio)
            tf = utils.processar_input_horario(f_fim)
            database.save_chamado(f_data.strftime('%Y-%m-%d'), f_caso, f_rid, f_hnome, ti, tf, f_obs)
            st.success(f"Registrado: {ti} - {tf}")
            st.rerun()

with tabs[1]:
    st.subheader("Histórico")
    rows = database.get_all_chamados()
    if rows:
        df_h = pd.DataFrame(rows, columns=['ID','Data','Caso','PMS','Hotel','Início','Término','Obs'])
        df_h['Data'] = pd.to_datetime(df_h['Data']).dt.strftime('%d/%m/%Y')
        st.dataframe(df_h.drop(columns=['ID']), use_container_width=True)
        with st.expander("Deletar Registro"):
            id_del = st.number_input("ID do registro", min_value=1)
            if st.button("Remover"):
                database.delete_chamado(id_del)
                st.rerun()

with tabs[2]:
    st.subheader("Gestão de Hotéis")
    if st.button("➕ Adicionar Hotel"): modal_novo_hotel()
    h_list = database.get_hoteis()
    for r, n in h_list:
        col_n, col_b1, col_b2 = st.columns([4, 1, 1])
        col_n.write(f"**{r}** - {n}")
        if col_b1.button("✏️", key=f"edh_{r}"): modal_editar_hotel(r, n)
        if col_b2.button("🗑️", key=f"dlh_{r}"): database.delete_hotel(r); st.rerun()

with tabs[3]:
    if st.session_state.user['admin']:
        st.subheader("Gestão de Usuários")
        if st.button("➕ Novo Usuário"): modal_novo_usuario()
        u_list = database.get_all_users()
        for uid, user, name, admin, must in u_list:
            cn, ca, cb1, cb2 = st.columns([3, 1, 0.5, 0.5])
            cn.write(f"**{user}** ({name})")
            ca.write("Admin" if admin else "User")
            if cb1.button("✏️", key=f"edu_{uid}"): modal_editar_usuario(uid, user, name, admin)
            if cb2.button("🗑️", key=f"dlu_{uid}"): database.delete_user(uid); st.rerun()
    else: st.info("Acesso restrito.")
