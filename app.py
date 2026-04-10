import streamlit as st
import pandas as pd
from datetime import datetime
import database
import utils
import report_generator

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO E INICIALIZAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Controle de Horas Extras", layout="wide")
database.init_db()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f4f4f4; }
    .header-style {
        color: #800000; text-align: center;
        padding-bottom: 16px; border-bottom: 2px solid #800000;
        margin-bottom: 24px; font-weight: 700; font-size: 1.4rem;
    }
    div[data-testid="stSidebarContent"] { background-color: #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GERENCIAMENTO DE SESSÃO
# ─────────────────────────────────────────────────────────────────────────────
_defaults = {
    'logged_in': False, 'user': None,
    'pdf_bytes': None, 'pdf_nome': None,
    # Controle de modais via session_state
    'modal_hotel_editar': None,   # None ou dict {rid, nome}
    'modal_hotel_novo': False,
    'modal_user_editar': None,    # None ou dict {uid, user, nome, admin}
    'modal_user_novo': False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Validar integridade da sessão
if st.session_state.logged_in and (
    not isinstance(st.session_state.user, dict)
    or 'nome' not in st.session_state.user
):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("<h1 class='header-style'>CONTROLE DE HORAS EXTRAS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### Acesso ao Sistema")
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("ENTRAR", use_container_width=True):
                user = database.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# TROCA DE SENHA OBRIGATÓRIA
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.user.get('must_change'):
    st.markdown("<h1 class='header-style'>TROCA DE SENHA OBRIGATÓRIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("pw_change"):
            np = st.text_input("Nova Senha", type="password")
            cp = st.text_input("Confirme a Senha", type="password")
            if st.form_submit_button("ALTERAR", use_container_width=True):
                if len(np) < 6:
                    st.error("A senha deve ter no mínimo 6 caracteres.")
                elif np != cp:
                    st.error("As senhas não coincidem.")
                else:
                    database.update_password(st.session_state.user['id'], np)
                    st.session_state.user['must_change'] = False
                    st.success("Senha alterada! Redirecionando...")
                    st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# MODAIS (st.dialog)
# ─────────────────────────────────────────────────────────────────────────────
@st.dialog("Novo Hotel")
def modal_novo_hotel():
    with st.form("form_novo_hotel", clear_on_submit=True):
        rid  = st.text_input("Código (RID)", value="")
        nome = st.text_input("Nome do Hotel", value="")
        if st.form_submit_button("CADASTRAR", use_container_width=True):
            if not rid or not nome:
                st.warning("Preencha todos os campos.")
            elif database.save_hotel(rid.strip(), nome.strip()):
                st.success("Hotel cadastrado!")
                st.session_state.modal_hotel_novo = False
                st.rerun()
            else:
                st.error("Código já existe.")

@st.dialog("Editar Hotel")
def modal_editar_hotel():
    dado = st.session_state.modal_hotel_editar  # {rid, nome}
    with st.form("form_edit_hotel"):
        new_rid  = st.text_input("Código (RID)", value=dado['rid'])
        new_nome = st.text_input("Nome do Hotel", value=dado['nome'])
        col_s, col_c = st.columns(2)
        salvar   = col_s.form_submit_button("SALVAR", use_container_width=True)
        cancelar = col_c.form_submit_button("CANCELAR", use_container_width=True)
        if salvar:
            if database.update_hotel(dado['rid'], new_rid.strip(), new_nome.strip()):
                st.success("Atualizado!")
                st.session_state.modal_hotel_editar = None
                st.rerun()
            else:
                st.error("Erro ao atualizar.")
        if cancelar:
            st.session_state.modal_hotel_editar = None
            st.rerun()

@st.dialog("Novo Usuário")
def modal_novo_usuario():
    with st.form("form_novo_user", clear_on_submit=True):
        user  = st.text_input("Usuário", value="")
        pw    = st.text_input("Senha Inicial", type="password")
        name  = st.text_input("Nome Completo", value="")
        admin = st.checkbox("Administrador", value=False)
        if st.form_submit_button("CRIAR", use_container_width=True):
            if not user or not pw or not name:
                st.warning("Preencha todos os campos.")
            elif database.create_user(user.strip(), pw, name.strip(), admin):
                st.success("Usuário criado!")
                st.session_state.modal_user_novo = False
                st.rerun()
            else:
                st.error("Usuário já existe.")

@st.dialog("Editar Usuário")
def modal_editar_usuario():
    dado = st.session_state.modal_user_editar  # {uid, user, nome, admin}
    with st.form("form_edit_user"):
        new_user  = st.text_input("Usuário", value=dado['user'])
        new_name  = st.text_input("Nome Completo", value=dado['nome'])
        new_admin = st.checkbox("Administrador", value=bool(dado['admin']))
        new_pw    = st.text_input("Nova Senha (em branco = manter)", type="password")
        col_s, col_c = st.columns(2)
        salvar   = col_s.form_submit_button("SALVAR", use_container_width=True)
        cancelar = col_c.form_submit_button("CANCELAR", use_container_width=True)
        if salvar:
            if database.update_user(dado['uid'], new_user.strip(), new_name.strip(), new_admin, new_pw or None):
                st.success("Usuário atualizado!")
                st.session_state.modal_user_editar = None
                st.rerun()
            else:
                st.error("Erro ao atualizar.")
        if cancelar:
            st.session_state.modal_user_editar = None
            st.rerun()

# ─── Disparar modais baseado no session_state ────────────────────────────────
if st.session_state.modal_hotel_novo:
    modal_novo_hotel()
if st.session_state.modal_hotel_editar is not None:
    modal_editar_hotel()
if st.session_state.modal_user_novo:
    modal_novo_usuario()
if st.session_state.modal_user_editar is not None:
    modal_editar_usuario()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user.get('nome', 'Usuário')}")
    if st.button("Sair", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📅 Relatório PDF")
    meses = ["JANEIRO","FEVEREIRO","MARÇO","ABRIL","MAIO","JUNHO",
             "JULHO","AGOSTO","SETEMBRO","OUTUBRO","NOVEMBRO","DEZEMBRO"]
    m_sel = st.selectbox("Mês Referente", meses, index=datetime.now().month - 1)
    a_sel = st.number_input("Ano", 2024, 2030, datetime.now().year)

    if st.button("🚀 GERAR PDF", use_container_width=True):
        try:
            rows  = database.get_all_chamados()
            df_p  = pd.DataFrame(rows, columns=['id','data','caso','pms','hotel','inicio','termino','observacoes'])
            df_ag = utils.agrupar_por_data(df_p, m_sel, a_sel)
            path  = f"folha_horas_{m_sel}_{a_sel}.pdf"
            report_generator.gerar_pdf(df_ag, st.session_state.user['nome'], m_sel, str(a_sel), path)
            with open(path, "rb") as f:
                st.session_state['pdf_bytes'] = f.read()
            st.session_state['pdf_nome'] = path
            st.success("PDF gerado!")
        except Exception as e:
            st.error(f"Erro: {e}")
            st.session_state['pdf_bytes'] = None

    if st.session_state.get('pdf_bytes'):
        st.download_button(
            "📂 Baixar PDF",
            data=st.session_state['pdf_bytes'],
            file_name=st.session_state.get('pdf_nome', 'Folha_Horas.pdf'),
            mime="application/pdf",
            use_container_width=True
        )

# ─────────────────────────────────────────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<h1 class='header-style'>CONTROLE DE HORAS EXTRAS</h1>", unsafe_allow_html=True)

# Carregar hotéis UMA VEZ (lista limpa a cada rerun, sem append global)
h_rows = database.get_hoteis()
h_opts = [f"{r} - {n}" for r, n in h_rows]

tabs = st.tabs(["📝 Novo Registro", "📋 Histórico", "🏨 Hotéis", "⚙️ Usuários"])

# ── Tab 0: Novo Registro ─────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("Inserir Novo Chamado")
    with st.form("novo_registro", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_data = st.date_input("Data do Atendimento", value=datetime.now())
            f_caso = st.text_input("Caso / INC (Opcional)")
        with c2:
            # Selectbox com placeholder e index=None (inicia em branco)
            f_hsel = st.selectbox(
                "Hotel / PMS",
                options=h_opts,
                index=None,
                placeholder="Selecione o hotel..."
            )
        with c3:
            f_inicio = st.text_input("Início (ex: 0800)", value="08:00")
            f_fim    = st.text_input("Término (ex: 1730)", value="17:00")
        f_obs = st.text_area("Observações")

        if st.form_submit_button("💾 SALVAR REGISTRO", use_container_width=True):
            if f_hsel is None:
                st.error("Selecione um hotel.")
            else:
                f_rid, f_hnome = f_hsel.split(" - ", 1) if " - " in f_hsel else ("", f_hsel)
                ti = utils.processar_input_horario(f_inicio)
                tf = utils.processar_input_horario(f_fim)
                database.save_chamado(
                    f_data.strftime('%Y-%m-%d'), f_caso or None,
                    f_rid, f_hnome, ti, tf, f_obs or None
                )
                st.success(f"✅ Registrado: {f_hnome} | {ti} → {tf}")
                st.rerun()

# ── Tab 1: Histórico ─────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Histórico de Registros")
    rows = database.get_all_chamados()
    if rows:
        df_h = pd.DataFrame(rows, columns=['ID','Data','Caso','PMS','Hotel','Início','Término','Obs'])
        df_h['Data'] = pd.to_datetime(df_h['Data']).dt.strftime('%d/%m/%Y')
        st.dataframe(df_h.drop(columns=['ID']), use_container_width=True, hide_index=True)
        st.markdown("---")
        with st.expander("🗑️ Remover Registro"):
            id_del = st.number_input("ID do registro a remover", min_value=1, step=1)
            if st.button("Remover", type="primary"):
                database.delete_chamado(int(id_del))
                st.success("Registro removido.")
                st.rerun()
    else:
        st.info("Nenhum registro encontrado.")

# ── Tab 2: Gestão de Hotéis ───────────────────────────────────────────────────
with tabs[2]:
    st.subheader("Gestão de Hotéis")
    if st.button("➕ Novo Hotel", type="primary"):
        st.session_state.modal_hotel_novo = True
        st.rerun()

    if h_rows:
        # Cabeçalho da tabela
        hdr = st.columns([1, 4, 1, 1])
        hdr[0].markdown("**Código**")
        hdr[1].markdown("**Nome**")
        st.markdown("---")

        # Listar hotéis com ações (SELECT DISTINCT já no banco via GROUP BY rid)
        for i, (r, n) in enumerate(h_rows):
            col_r, col_n, col_e, col_d = st.columns([1, 4, 1, 1])
            col_r.write(r)
            col_n.write(n)
            if col_e.button("✏️", key=f"edh_{i}", help="Editar"):
                st.session_state.modal_hotel_editar = {'rid': r, 'nome': n}
                st.rerun()
            if col_d.button("🗑️", key=f"dlh_{i}", help="Excluir"):
                database.delete_hotel(r)
                st.rerun()
    else:
        st.info("Nenhum hotel cadastrado.")

# ── Tab 3: Gestão de Usuários ─────────────────────────────────────────────────
with tabs[3]:
    if st.session_state.user.get('admin'):
        st.subheader("Gestão de Usuários")
        if st.button("➕ Novo Usuário", type="primary"):
            st.session_state.modal_user_novo = True
            st.rerun()

        u_list = database.get_all_users()
        if u_list:
            st.markdown("---")
            for uid, uname, unom, uadm, umust in u_list:
                cu, cn, cp, ce, cd = st.columns([1.5, 2.5, 1, 0.6, 0.6])
                cu.write(f"**{uname}**")
                cn.write(unom)
                cp.write("🔴 Admin" if uadm else "🟢 User")
                if ce.button("✏️", key=f"edu_{uid}", help="Editar"):
                    st.session_state.modal_user_editar = {
                        'uid': uid, 'user': uname, 'nome': unom, 'admin': uadm
                    }
                    st.rerun()
                if cd.button("🗑️", key=f"dlu_{uid}", help="Excluir"):
                    database.delete_user(uid)
                    st.rerun()
    else:
        st.info("Acesso restrito a administradores.")
