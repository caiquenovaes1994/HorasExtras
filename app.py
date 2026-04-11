import streamlit as st
import pandas    as pd
from datetime    import datetime
import os

import database
import utils
import report_generator

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Controle de Horas Extras", layout="wide")

@st.cache_resource
def _init_db_once():
    """Inicializa o banco de dados apenas uma vez por sessão do servidor."""
    database.init_db()

_init_db_once()

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

/* Ocultar Elementos de Sistema (User Request) */
.stAppDeployButton { display: none !important; }
#stStatusWidget { display: none !important; }
[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; color: #800000 !important; }
footer { visibility: hidden; }

/* Esconder opções específicas do menu (Record, Print, etc) */
div[data-testid="stToolbar"] { display: none !important; }

/* Botão Lápis Sidebar (Sem contorno) */
button[help="Editar perfil"] {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
}
button[help="Editar perfil"]:hover {
    background: rgba(255,255,255,0.1) !important;
}
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
    "dlg_user_editar":    None,   # {"uid": …, "user": …, "nome": …, "admin": …, "valor_base": …}
    "dlg_perfil_editar":  False,
    "dlg_reg_editar":     None,   # ID do registro
    "dlg_reg_deletar":    None,   # ID do registro
    # Campos do formulário de registro (Persistência)
    "reg_data":           datetime.now(),
    "reg_caso":           "",
    "reg_hotel":          None,
    "reg_motivo":         "",
    "reg_inicio":         "",
    "reg_termino":        "",
    "reg_obs":            "",
    "reg_reset":          False,
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

@st.dialog("Sugerir Novo Hotel")
def _dlg_novo_hotel():
    with st.form("frm_novo_hotel", clear_on_submit=True):
        rid  = st.text_input("RID")
        nome = st.text_input("Nome do Hotel")
        ok   = st.form_submit_button("SOLICITAR CADASTRO", use_container_width=True)
    if ok:
        if not rid.strip() or not nome.strip():
            st.warning("Preencha RID e nome.")
        else:
            database.criar_solicitacao_hotel(rid.strip(), nome.strip(), 'CREATE', st.session_state.user["id"])
            st.success("Solicitação enviada para aprovação!")
            st.session_state.dlg_hotel_novo = False
            st.rerun()


@st.dialog("Sugerir Edição de Hotel")
def _dlg_editar_hotel():
    d = st.session_state.dlg_hotel_editar
    with st.form("frm_edit_hotel"):
        new_rid  = st.text_input("RID (Não alterável)", value=d["rid"], disabled=True)
        new_nome = st.text_input("Novo Nome do Hotel",  value=d["nome"])
        c1, c2   = st.columns(2)
        salvar   = c1.form_submit_button("SOLICITAR ALTERAÇÃO", use_container_width=True)
        cancelar = c2.form_submit_button("CANCELAR", use_container_width=True)
    if salvar:
        database.criar_solicitacao_hotel(d["rid"], new_nome.strip(), 'EDIT', st.session_state.user["id"])
        st.success("Solicitação de edição enviada!")
        st.session_state.dlg_hotel_editar = None
        st.rerun()
    if cancelar:
        st.session_state.dlg_hotel_editar = None
        st.rerun()


@st.dialog("Novo Usuário")
def _dlg_novo_usuario():
    with st.form("frm_novo_user", clear_on_submit=True):
        uname = st.text_input("Usuário (login)")
        pw    = st.text_input("Senha inicial", type="password")
        nome  = st.text_input("Nome Completo")
        vbase = st.number_input("Salário Mensal (R$)", min_value=0.0, step=0.1, format="%.2f")
        adm   = st.checkbox("Administrador")
        ok    = st.form_submit_button("CRIAR", use_container_width=True)
    if ok:
        if not uname.strip() or not pw or not nome.strip():
            st.warning("Preencha todos os campos.")
        elif database.create_user(uname.strip(), pw, nome.strip(), adm, vbase):
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
        new_vbase = st.number_input("Salário Mensal (R$)", value=float(d["valor_base"]), min_value=0.0, step=0.1, format="%.2f")
        new_adm   = st.checkbox("Administrador",    value=bool(d["admin"]))
        new_pw    = st.text_input("Nova Senha (em branco = manter)", type="password")
        c1, c2    = st.columns(2)
        salvar    = c1.form_submit_button("SALVAR",   use_container_width=True)
        cancelar  = c2.form_submit_button("CANCELAR", use_container_width=True)
    if salvar:
        if database.update_user(d["uid"], new_uname.strip(), new_nome.strip(),
                                new_adm, new_vbase, new_pw or None):
            st.success("Atualizado!")
            st.session_state.dlg_user_editar = None
            st.rerun()
        else:
            st.error("Erro ao atualizar.")
    if cancelar:
        st.session_state.dlg_user_editar = None
        st.rerun()

@st.dialog("Editar Meu Perfil")
def _dlg_editar_perfil():
    u = st.session_state.user
    is_admin = u.get("admin")
    with st.form("frm_edit_self"):
        # Usuários comuns não alteram login nem nome
        if is_admin:
            new_nome  = st.text_input("Nome Completo", value=u.get("nome"))
            new_uname = st.text_input("Usuário (Login)", value=u.get("username"))
        else:
            st.info(f"Nome: {u.get('nome')}")
            st.info(f"Usuário: {u.get('username')}")
            new_nome  = u.get("nome")
            new_uname = u.get("username")
            
        new_vbase = st.number_input("Salário Mensal (R$)", value=float(u.get("valor_base", 0.0)), min_value=0.0, step=0.1, format="%.2f")
        new_pw    = st.text_input("Alterar Minha Senha (em branco = manter)", type="password")
        c1, c2 = st.columns(2)
        if c1.form_submit_button("SALVAR", use_container_width=True):
            if database.update_user(u["id"], new_uname, new_nome, u["admin"], new_vbase, new_pw or None):
                st.session_state.user["nome"] = new_nome
                st.session_state.user["username"] = new_uname
                st.session_state.user["valor_base"] = new_vbase
                st.success("Perfil atualizado!")
                st.session_state.dlg_perfil_editar = False
                st.rerun()
            else:
                st.error("Erro ao salvar perfil.")
        if c2.form_submit_button("FECHAR", use_container_width=True):
            st.session_state.dlg_perfil_editar = False
            st.rerun()

@st.dialog("Editar Registro")
def _dlg_editar_registro():
    cid = st.session_state.dlg_reg_editar
    row = database.get_chamado_by_id(cid)
    if not row:
        st.error("Registro não encontrado.")
        if st.button("Fechar"):
            st.session_state.dlg_reg_editar = None
            st.rerun()
        return

    # row structure: (id, data, caso, pms, hotel, inicio, termino, obs)
    with st.form("frm_edit_reg"):
        f_data = st.date_input("Data", value=datetime.strptime(row[1], "%Y-%m-%d"))
        f_caso = st.text_input("Caso / INC", value=row[2] or "")
        
        h_rows = database.get_hoteis()
        h_opts = [f"{r} - {n}" for r, n in h_rows]
        current_h = f"{row[3]} - {row[4]}"
        try:
            h_idx = h_opts.index(current_h)
        except:
            h_idx = None
            
        f_hsel = st.selectbox("Hotel / PMS", options=h_opts, index=h_idx)
        c1, c2 = st.columns(2)
        f_inicio = c1.text_input("Início", value=row[5])
        f_fim    = c2.text_input("Término", value=row[6])
        f_obs    = st.text_area("Observações", value=row[7] or "")
        
        cb1, cb2 = st.columns(2)
        if cb1.form_submit_button("SALVAR", use_container_width=True):
            rid_, hnome_ = (f_hsel.split(" - ", 1) if f_hsel and " - " in f_hsel else ("", f_hsel))
            database.update_chamado(cid, f_data.strftime("%Y-%m-%d"), f_caso.strip(), rid_, hnome_, 
                                    utils.processar_input_horario(f_inicio), 
                                    utils.processar_input_horario(f_fim), f_obs.strip())
            st.success("Atualizado!")
            st.session_state.dlg_reg_editar = None
            st.rerun()
        if cb2.form_submit_button("CANCELAR", use_container_width=True):
            st.session_state.dlg_reg_editar = None
            st.rerun()


@st.dialog("Confirmar Exclusão")
def _dlg_confirmar_delecao():
    cid = st.session_state.dlg_reg_deletar
    st.warning(f"Tem certeza que deseja excluir o registro ID {cid}?")
    c1, c2 = st.columns(2)
    if c1.button("SIM, EXCLUIR", use_container_width=True, type="primary"):
        database.delete_chamado(cid)
        st.success("Removido!")
        st.session_state.dlg_reg_deletar = None
        st.rerun()
    if c2.button("NÃO", use_container_width=True):
        st.session_state.dlg_reg_deletar = None
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
if st.session_state.dlg_perfil_editar:
    _dlg_editar_perfil()
if st.session_state.dlg_reg_editar is not None:
    _dlg_editar_registro()
if st.session_state.dlg_reg_deletar is not None:
    _dlg_confirmar_delecao()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    u = st.session_state.user
    c1, c2 = st.columns([4, 1])
    c1.markdown(f"### 👤 {u.get('nome', 'Usuário')}")
    if c2.button("✏️", help="Editar perfil"):
        st.session_state.dlg_perfil_editar = True
        st.rerun()

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
                columns=["id","data","caso","pms","hotel","inicio","termino","observacoes", "motivo"]
            )
            df_ag = utils.agrupar_por_data(df, m_sel, a_sel)
            path  = f"folha_horas_{m_sel}_{a_sel}.pdf"
            report_generator.gerar_pdf(df_ag, u["nome"], m_sel, str(a_sel), u.get("valor_base", 0.0), path)
            with open(path, "rb") as fh:
                st.session_state["pdf_bytes"] = fh.read()
            st.session_state["pdf_nome"] = path
            
            # DELEÇÃO IMEDIATA: Remove o arquivo físico após carregar os bytes para a memória da sessão
            if os.path.exists(path):
                os.remove(path)
                
            st.success("✅ PDF gerado e pronto para download!")
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

TABS_LIST = ["📝 Novo Registro", "📋 Histórico", "🏨 Hotéis", "⚙️ Usuários"]
if st.session_state.user.get("admin"):
    TABS_LIST.append("🔔 Aprovações")

TABS = st.tabs(TABS_LIST)


# ── ABA 0 – Novo Registro ─────────────────────────────────────────────────────
with TABS[0]:
    # Lógica de Reset Seguro (Evita erro de 'instantiated widget')
    if st.session_state.get("reg_reset"):
        st.session_state.reg_data    = datetime.now()
        st.session_state.reg_caso    = ""
        st.session_state.reg_hotel   = None
        st.session_state.reg_motivo  = ""
        st.session_state.reg_inicio  = ""
        st.session_state.reg_termino = ""
        st.session_state.reg_obs     = ""
        st.session_state.reg_reset   = False

    st.subheader("Inserir Novo Chamado")
    with st.form("frm_novo_reg", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            f_data   = st.date_input("Data do Atendimento", format="DD/MM/YYYY", key="reg_data")
            f_caso   = st.text_input("Caso / INC", placeholder="Opcional", key="reg_caso")
            f_hsel   = st.selectbox("Hotel", options=h_opts, index=None, placeholder="Opcional: Selecione ou busque o hotel…", key="reg_hotel")
            f_motivo = st.text_input("Motivo * (Uso Interno)", placeholder="Descreva o motivo do chamado...", key="reg_motivo")
        with c2:
            f_inicio  = st.text_input("Início *",  placeholder="08:00", key="reg_inicio")
            f_fim     = st.text_input("Término *", placeholder="17:00", key="reg_termino")
            f_obs     = st.text_area("Observações (PDF)", placeholder="Opcional", height=138, key="reg_obs")

        if st.form_submit_button("💾 SALVAR", use_container_width=True):
            if not f_inicio or not f_fim or not f_motivo.strip():
                st.error("Campos obrigatórios: Início, Término e Motivo.")
            else:
                try:
                    rid_, hnome_ = ("", "")
                    if f_hsel:
                        rid_, hnome_ = (f_hsel.split(" - ", 1) if " - " in f_hsel else ("", f_hsel))
                    
                    ti = utils.processar_input_horario(f_inicio)
                    tf = utils.processar_input_horario(f_fim)
                    database.save_chamado(
                        f_data.strftime("%Y-%m-%d"),
                        f_caso.strip() or None,
                        rid_, hnome_, ti, tf,
                        f_obs.strip() or None,
                        f_motivo.strip()
                    )
                    st.success(f"✅ Registrado!")
                    # Ativa o reset para a próxima execução (evita o erro de widget instanciado)
                    st.session_state.reg_reset = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")


# ── ABA 1 – Histórico ────────────────────────────────────────────────────────
with TABS[1]:
    rows_all = database.get_all_chamados()
    if rows_all:
        # Filtros de Histórico
        c_h1, c_h2 = st.columns(2)
        with c_h1:
            m_hist = st.selectbox("Mês", options=["TODOS", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], index=0)
        with c_h2:
            a_hist = st.number_input("Ano", value=datetime.now().year, step=1)
        
        # Lógica de Filtragem no Histórico
        rows = []
        for r in rows_all:
            # id, data, caso, rid, hotel, inicio, termino, obs, motivo
            dt_obj = datetime.strptime(r[1], "%Y-%m-%d")
            if a_hist and dt_obj.year != a_hist:
                continue
            if m_hist != "TODOS":
                meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
                if meses[dt_obj.month - 1] != m_hist:
                    continue
            rows.append(r)
            
        if rows:
            # Tabela com botões de ação
            cols = st.columns([1, 1, 1.8, 1, 1, 1.5, 1.2])
            headers = ["Data", "Caso", "Hotel", "Início", "Término", "Obs", "Ações"]
            for col, h in zip(cols, headers):
                col.markdown(f"**{h}**")
            st.divider()
            
            for r in rows:
                # id, data, caso, pms, hotel, inicio, termino, obs, motivo
                c1, c2, c4, c5, c6, c7, c8 = st.columns([1, 1, 1.8, 1, 1, 1.5, 1.2])
                dt_fmt = datetime.strptime(r[1], "%Y-%m-%d").strftime("%d/%m/%Y")
                c1.write(dt_fmt)
                c2.write(r[2] or "—")
                # Hotel formatado como RID - Nome
                c4.write(f"{r[3]} - {r[4]}")
                c5.write(r[5])
                c6.write(r[6])
                c7.write(r[7] or "—")
                
                # Botões de ação
                bt_ed, bt_del = c8.columns(2)
                if bt_ed.button("✏️", key=f"ed_reg_{r[0]}", help="Editar registro"):
                    st.session_state.dlg_reg_editar = r[0]
                    st.rerun()
                if bt_del.button("🗑️", key=f"del_reg_{r[0]}", help="Excluir registro"):
                    st.session_state.dlg_reg_deletar = r[0]
                    st.rerun()
    else:
        st.info("Nenhum registro encontrado.")


# ── ABA 2 – Hotéis ───────────────────────────────────────────────────────────
with TABS[2]:
    st.subheader("Gestão de Hotéis")
    if st.button("➕ Sugerir Novo Hotel", type="primary"):
        st.session_state.dlg_hotel_novo = True
        st.rerun()

    if h_rows:
        c_cod, c_nom, c_ed, c_del = st.columns([1.2, 5, 0.6, 0.6])
        c_cod.markdown("**RID**"); c_nom.markdown("**Nome**")
        st.divider()
        for i, (r, n) in enumerate(h_rows):
            ca, cb, cc, cd = st.columns([1.2, 5, 0.6, 0.6])
            ca.write(r); cb.write(n)
            if cc.button("✏️", key=f"edh_{i}", help="Sugerir alteração"):
                st.session_state.dlg_hotel_editar = {"rid": r, "nome": n}
                st.rerun()
            if cd.button("🗑️", key=f"dlh_{i}", help="Solicitar exclusão"):
                database.criar_solicitacao_hotel(r, n, 'DELETE', st.session_state.user["id"])
                st.info("Solicitação de exclusão enviada.")
                st.rerun()
    else:
        st.info("Nenhum hotel cadastrado ou aprovado.")


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
            for uid, uname, unom, uadm, umust, uvb in u_list:
                cu, cn, cp, ce, cr, cx = st.columns([1.5, 2.5, 1, 0.6, 0.6, 0.6])
                cu.write(f"**{uname}**")
                cn.write(unom or "—")
                # Exibe perfil na lista
                cp.write("🔴 Admin" if uadm else "🟢 User")
                if ce.button("✏️", key=f"edu_{uid}", help="Editar"):
                    st.session_state.dlg_user_editar = {
                        "uid": uid, "user": uname, "nome": unom, "admin": uadm, "valor_base": uvb
                    }
                    st.rerun()
                if cr.button("🔑", key=f"resetu_{uid}", help="Resetar Senha para 'mudar123'"):
                    database.reset_password_admin(uid)
                    st.success(f"Senha de {uname} resetada para 'mudar123'!")
                if cx.button("🗑️", key=f"dlu_{uid}", help="Excluir"):
                    database.delete_user(uid)
                    st.rerun()
    else:
        st.info("Acesso restrito a administradores.")

if st.session_state.user.get("admin"):
    with TABS[4]:
        st.subheader("🔔 Aprovações Pendentes (Hotéis)")
        sols = database.get_solicitacoes_pendentes()
        if sols:
            c1, c2, c3, c4, c5 = st.columns([1, 2.5, 1, 2, 2])
            c1.markdown("**RID**"); c2.markdown("**Nome**"); c3.markdown("**Ação**"); c4.markdown("**Usuário**")
            st.divider()
            for sid, srid, snome, stipo, sunom in sols:
                ca, cb, cc, cd, ce = st.columns([1, 2.5, 1, 2, 2])
                ca.write(srid); cb.write(snome); cc.write(stipo); cd.write(sunom)
                bt_ap, bt_rj = ce.columns(2)
                if bt_ap.button("✅", key=f"ap_{sid}"):
                    database.processar_solicitacao(sid, True)
                    st.rerun()
                if bt_rj.button("❌", key=f"rj_{sid}"):
                    database.processar_solicitacao(sid, False)
                    st.rerun()
        else:
            st.info("Nenhuma solicitação pendente.")
