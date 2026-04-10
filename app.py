import streamlit as st
import pandas    as pd
from datetime    import datetime

import database
import utils
import report_generator

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Controle de Horas Extras", layout="wide")
database.init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #f2f2f2; }
h1.page-title {
    color: #800000; text-align: center;
    border-bottom: 2px solid #800000;
    padding-bottom: 10px; margin-bottom: 20px;
    font-weight: 700; font-size: 1.35rem; letter-spacing: .04em;
}
/* Sidebar escura */
section[data-testid="stSidebar"] > div {
    background-color: #1c1c1c;
    color: #ececec;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #ececec; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE — valores padrão
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS: dict = {
    "logged_in":          False,
    "user":               None,
    "pdf_bytes":          None,
    "pdf_nome":           None,
    # Modais: None = fechado · dict = dados para edição
    "dlg_hotel_novo":     False,
    "dlg_hotel_editar":   None,   # {"rid": …, "nome": …}
    "dlg_user_novo":      False,
    "dlg_user_editar":    None,   # {"uid": …, "user": …, "nome": …, "admin": …}
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# Valida integridade da sessão (protege contra versões antigas no cache)
if st.session_state.logged_in and (
    not isinstance(st.session_state.user, dict)
    or "nome" not in st.session_state.user
):
    st.session_state.logged_in = False
    st.session_state.user      = None
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown('<h1 class="page-title">CONTROLE DE HORAS EXTRAS</h1>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("##### Acesso ao Sistema")
        with st.form("frm_login"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("ENTRAR", use_container_width=True):
                u = database.verify_login(username, password)
                if u:
                    st.session_state.logged_in = True
                    st.session_state.user      = u
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# TROCA DE SENHA OBRIGATÓRIA
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.user.get("must_change"):
    st.markdown('<h1 class="page-title">TROCA DE SENHA OBRIGATÓRIA</h1>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.form("frm_troca_senha"):
            np1 = st.text_input("Nova Senha", type="password")
            np2 = st.text_input("Confirme a Nova Senha", type="password")
            if st.form_submit_button("ALTERAR", use_container_width=True):
                if len(np1) < 6:
                    st.error("Mínimo de 6 caracteres.")
                elif np1 != np2:
                    st.error("As senhas não coincidem.")
                else:
                    database.update_password(st.session_state.user["id"], np1)
                    st.session_state.user["must_change"] = False
                    st.success("Senha alterada! Redirecionando…")
                    st.rerun()
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# MODAIS  (st.dialog)
# ─────────────────────────────────────────────────────────────────────────────

@st.dialog("Novo Hotel")
def _dlg_novo_hotel():
    with st.form("frm_novo_hotel", clear_on_submit=True):
        rid  = st.text_input("Código RID")
        nome = st.text_input("Nome do Hotel")
        ok   = st.form_submit_button("CADASTRAR", use_container_width=True)
    if ok:
        if not rid.strip() or not nome.strip():
            st.warning("Preencha código e nome.")
        elif database.save_hotel(rid.strip(), nome.strip()):
            st.success("Hotel cadastrado!")
            st.session_state.dlg_hotel_novo = False
            st.rerun()
        else:
            st.error("Código já existe.")


@st.dialog("Editar Hotel")
def _dlg_editar_hotel():
    d = st.session_state.dlg_hotel_editar
    with st.form("frm_edit_hotel"):
        new_rid  = st.text_input("Código RID",     value=d["rid"])
        new_nome = st.text_input("Nome do Hotel",  value=d["nome"])
        c1, c2   = st.columns(2)
        salvar   = c1.form_submit_button("SALVAR",   use_container_width=True)
        cancelar = c2.form_submit_button("CANCELAR", use_container_width=True)
    if salvar:
        if database.update_hotel(d["rid"], new_rid.strip(), new_nome.strip()):
            st.success("Atualizado!")
            st.session_state.dlg_hotel_editar = None
            st.rerun()
        else:
            st.error("Erro ao atualizar.")
    if cancelar:
        st.session_state.dlg_hotel_editar = None
        st.rerun()


@st.dialog("Novo Usuário")
def _dlg_novo_usuario():
    with st.form("frm_novo_user", clear_on_submit=True):
        uname = st.text_input("Usuário (login)")
        pw    = st.text_input("Senha inicial", type="password")
        nome  = st.text_input("Nome Completo")
        adm   = st.checkbox("Administrador")
        ok    = st.form_submit_button("CRIAR", use_container_width=True)
    if ok:
        if not uname.strip() or not pw or not nome.strip():
            st.warning("Preencha todos os campos.")
        elif database.create_user(uname.strip(), pw, nome.strip(), adm):
            st.success("Usuário criado!")
            st.session_state.dlg_user_novo = False
            st.rerun()
        else:
            st.error("Usuário já existe.")


@st.dialog("Editar Usuário")
def _dlg_editar_usuario():
    d = st.session_state.dlg_user_editar
    with st.form("frm_edit_user"):
        new_uname = st.text_input("Usuário",        value=d["user"])
        new_nome  = st.text_input("Nome Completo",  value=d["nome"])
        new_adm   = st.checkbox("Administrador",    value=bool(d["admin"]))
        new_pw    = st.text_input("Nova Senha (em branco = manter)", type="password")
        c1, c2    = st.columns(2)
        salvar    = c1.form_submit_button("SALVAR",   use_container_width=True)
        cancelar  = c2.form_submit_button("CANCELAR", use_container_width=True)
    if salvar:
        if database.update_user(d["uid"], new_uname.strip(), new_nome.strip(),
                                new_adm, new_pw or None):
            st.success("Atualizado!")
            st.session_state.dlg_user_editar = None
            st.rerun()
        else:
            st.error("Erro ao atualizar.")
    if cancelar:
        st.session_state.dlg_user_editar = None
        st.rerun()


# Disparar modais conforme session_state
if st.session_state.dlg_hotel_novo:
    _dlg_novo_hotel()
if st.session_state.dlg_hotel_editar is not None:
    _dlg_editar_hotel()
if st.session_state.dlg_user_novo:
    _dlg_novo_usuario()
if st.session_state.dlg_user_editar is not None:
    _dlg_editar_usuario()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    u = st.session_state.user
    st.markdown(f"### 👤 {u.get('nome', 'Usuário')}")

    if st.button("Sair", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📅 Relatório PDF")

    MESES = ["JANEIRO","FEVEREIRO","MARÇO","ABRIL","MAIO","JUNHO",
             "JULHO","AGOSTO","SETEMBRO","OUTUBRO","NOVEMBRO","DEZEMBRO"]
    m_sel = st.selectbox("Mês Referente", MESES, index=datetime.now().month - 1)
    a_sel = st.number_input("Ano", 2024, 2030, datetime.now().year)

    if st.button("🚀 GERAR PDF", use_container_width=True):
        try:
            rows  = database.get_all_chamados()
            df    = pd.DataFrame(
                rows,
                columns=["id","data","caso","pms","hotel","inicio","termino","observacoes"]
            )
            df_ag = utils.agrupar_por_data(df, m_sel, a_sel)
            path  = f"folha_horas_{m_sel}_{a_sel}.pdf"
            report_generator.gerar_pdf(df_ag, u["nome"], m_sel, str(a_sel), path)
            with open(path, "rb") as fh:
                st.session_state["pdf_bytes"] = fh.read()
            st.session_state["pdf_nome"] = path
            st.success("✅ PDF gerado!")
        except Exception as ex:
            import traceback
            st.error(f"Erro ao gerar PDF:\n{ex}")
            st.code(traceback.format_exc(), language="python")
            st.session_state["pdf_bytes"] = None

    if st.session_state.get("pdf_bytes"):
        st.download_button(
            "📂 Baixar PDF",
            data=st.session_state["pdf_bytes"],
            file_name=st.session_state.get("pdf_nome", "Folha_Horas.pdf"),
            mime="application/pdf",
            use_container_width=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="page-title">CONTROLE DE HORAS EXTRAS</h1>', unsafe_allow_html=True)

# Hotéis carregados UMA VEZ por rerun (lista limpa, sem append global)
h_rows = database.get_hoteis()
h_opts = [f"{r} - {n}" for r, n in h_rows]

TABS = st.tabs(["📝 Novo Registro", "📋 Histórico", "🏨 Hotéis", "⚙️ Usuários"])


# ── ABA 0 – Novo Registro ─────────────────────────────────────────────────────
with TABS[0]:
    st.subheader("Inserir Novo Chamado")
    with st.form("frm_novo_reg", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_data = st.date_input("Data do Atendimento", value=datetime.now())
            # Campo INC opcional
            f_caso = st.text_input("Caso / INC", placeholder="Opcional")
        with c2:
            # Inicia em branco; filtra ao digitar
            f_hsel = st.selectbox(
                "Hotel / PMS",
                options=h_opts,
                index=None,
                placeholder="Selecione ou busque o hotel…"
            )
        with c3:
            # Máscara aplicada ao salvar (0800 → 08:00)
            f_inicio = st.text_input("Início",  placeholder="08:00 ou 0800", value="")
            f_fim    = st.text_input("Término", placeholder="17:00 ou 1730", value="")
        f_obs = st.text_area("Observações", placeholder="Opcional")

        if st.form_submit_button("💾 SALVAR", use_container_width=True):
            if f_hsel is None:
                st.error("Selecione um hotel antes de salvar.")
            else:
                rid_, hnome_ = (f_hsel.split(" - ", 1) if " - " in f_hsel else ("", f_hsel))
                ti = utils.processar_input_horario(f_inicio or "00:00")
                tf = utils.processar_input_horario(f_fim    or "00:00")
                database.save_chamado(
                    f_data.strftime("%Y-%m-%d"),
                    f_caso.strip() or None,
                    rid_, hnome_, ti, tf,
                    f_obs.strip() or None,
                )
                st.success(f"✅ Registrado — {hnome_} | {ti} → {tf}")
                st.rerun()


# ── ABA 1 – Histórico ────────────────────────────────────────────────────────
with TABS[1]:
    st.subheader("Histórico de Registros")
    rows = database.get_all_chamados()
    if rows:
        df_h = pd.DataFrame(
            rows,
            columns=["ID","Data","Caso","PMS","Hotel","Início","Término","Obs"]
        )
        df_h["Data"] = pd.to_datetime(df_h["Data"]).dt.strftime("%d/%m/%Y")
        st.dataframe(df_h.drop(columns=["ID"]), use_container_width=True, hide_index=True)
        st.markdown("---")
        with st.expander("🗑️ Remover um registro"):
            id_del = st.number_input("ID do registro", min_value=1, step=1)
            if st.button("Remover", type="primary"):
                database.delete_chamado(int(id_del))
                st.success("Removido.")
                st.rerun()
    else:
        st.info("Nenhum registro encontrado.")


# ── ABA 2 – Hotéis ───────────────────────────────────────────────────────────
with TABS[2]:
    st.subheader("Gestão de Hotéis")
    if st.button("➕ Novo Hotel", type="primary"):
        st.session_state.dlg_hotel_novo = True
        st.rerun()

    if h_rows:
        c_cod, c_nom, c_ed, c_del = st.columns([1.2, 5, 0.6, 0.6])
        c_cod.markdown("**Código**"); c_nom.markdown("**Nome**")
        st.divider()
        for i, (r, n) in enumerate(h_rows):
            ca, cb, cc, cd = st.columns([1.2, 5, 0.6, 0.6])
            ca.write(r); cb.write(n)
            if cc.button("✏️", key=f"edh_{i}", help="Editar hotel"):
                st.session_state.dlg_hotel_editar = {"rid": r, "nome": n}
                st.rerun()
            if cd.button("🗑️", key=f"dlh_{i}", help="Excluir hotel"):
                database.delete_hotel(r)
                st.rerun()
    else:
        st.info("Nenhum hotel cadastrado.")


# ── ABA 3 – Usuários ─────────────────────────────────────────────────────────
with TABS[3]:
    if st.session_state.user.get("admin"):
        st.subheader("Gestão de Usuários")
        if st.button("➕ Novo Usuário", type="primary"):
            st.session_state.dlg_user_novo = True
            st.rerun()

        u_list = database.get_all_users()
        if u_list:
            st.divider()
            for uid, uname, unom, uadm, umust in u_list:
                cu, cn, cp, ce, cx = st.columns([1.5, 2.5, 1, 0.6, 0.6])
                cu.write(f"**{uname}**")
                cn.write(unom or "—")
                cp.write("🔴 Admin" if uadm else "🟢 User")
                if ce.button("✏️", key=f"edu_{uid}", help="Editar"):
                    st.session_state.dlg_user_editar = {
                        "uid": uid, "user": uname, "nome": unom, "admin": uadm
                    }
                    st.rerun()
                if cx.button("🗑️", key=f"dlu_{uid}", help="Excluir"):
                    database.delete_user(uid)
                    st.rerun()
    else:
        st.info("Acesso restrito a administradores.")
