import streamlit as st
import pandas    as pd
from datetime    import datetime, timedelta
import os
import extra_streamlit_components as stx
import time
import re

import database
import utils
import report_generator

# Captura o horário de São Paulo (Brasília) com fallback seguro
try:
    import pytz
    fuso_sp = pytz.timezone('America/Sao_Paulo')
    data_atual_sp = datetime.now(fuso_sp)
except ImportError:
    try:
        from zoneinfo import ZoneInfo
        data_atual_sp = datetime.now(ZoneInfo('America/Sao_Paulo'))
    except ImportError:
        data_atual_sp = datetime.now()

mes_atual = data_atual_sp.month
ano_atual = data_atual_sp.year

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Controle de Horas Extras", layout="wide", initial_sidebar_state="expanded")

@st.cache_resource
def _init_db_once():
    """Inicializa o banco de dados apenas uma vez por sessão do servidor."""
    database.init_db()

_init_db_once()

@st.cache_data(ttl=86400)
def get_cached_hoteis():
    """Cache de longa duração para lista de hotéis (24h)."""
    return database.get_hoteis()

@st.cache_data(ttl=300)
def get_cached_chamados(username_filter=None, perfil=None, logged_username=None):
    """Cache de curta duração para chamados do histórico (5min)."""
    return database.get_all_chamados(username_filter, perfil, logged_username)

# Inicializa o CookieManager
cookie_manager = stx.CookieManager(key="cookie_manager_primary")

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

footer { visibility: hidden; }

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
    "dlg_reg_ver":        None,   # ID do registro
    "dlg_reg_editar":     None,   # ID do registro
    "dlg_reg_deletar":    None,   # ID do registro
    "dlg_bulk_delete":    False,
    "selected_records":   set(),
    # Campos do formulário de registro (Persistência)
    "reg_data":           datetime.now(),
    "reg_caso":           "",
    "reg_hotel":          None,
    "reg_motivo":         "",
    "reg_inicio":         "",
    "reg_termino":        "",
    "reg_obs":            "",
    "reg_reset":          False,
    "logout_lock":        False,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# Lógica do Auto-Login por Cookies (Ignora se o usuário acabou de clicar em Sair)
auth_token = cookie_manager.get(cookie="auth_token")
if not st.session_state.logged_in and auth_token and not st.session_state.get("logout_lock"):
    username = database.decrypt_str(auth_token)
    if username:
        user_data = database.get_user_by_username(username)
        if user_data:
            st.session_state.logged_in = True
            st.session_state.user = user_data
            st.rerun()

# Valida integridade da sessão (protege contra versões antigas no cache)
if st.session_state.get("logged_in") and (
    not isinstance(st.session_state.user, dict)
    or "nome" not in st.session_state.user
):
    st.session_state.logged_in = False
    st.session_state.user      = None
    cookie_manager.delete("auth_token")
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
                    st.session_state.logout_lock = False
                    
                    # Salva cookie gerando um token seguro válido por 24 horas
                    token = database.encrypt_str(u["username"])
                    expires = datetime.now() + timedelta(hours=24)
                    cookie_manager.set("auth_token", token, expires_at=expires, path="/")
                    time.sleep(0.5) 
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
# ACEITE DE TERMOS DE USO (LGPD)
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.user.get("aceitou_termos"):
    st.markdown('<h1 class="page-title">TERMOS DE USO E POLÍTICA DE PRIVACIDADE</h1>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.warning(
            "### Resumo Importante (LGPD)\n\n"
            "Ao utilizar este sistema, você concorda com o registro de suas jornadas de trabalho "
            "e com a criptografia de seus dados financeiros (como salário base). "
            "Essas medidas visam a segurança jurídica e a conformidade com a LGPD."
        )
        
        with st.expander("📄 Ler Termos de Uso e Política de Privacidade Completos"):
            st.markdown(
                "#### 1. Coleta de Dados\n"
                "Coletamos dados de identificação (nome, usuário) e registros de jornada (horários de início e término) "
                "estritamente para o cálculo de horas extras.\n\n"
                "#### 2. Segurança\n"
                "Seus dados financeiros são armazenados de forma criptografada (AES-256) no banco de dados.\n\n"
                "#### 3. Direitos do Titular\n"
                "Você pode solicitar a revisão ou exclusão de seus dados conforme a LGPD, desde que "
                "não conflitem com obrigações legais de registro de ponto."
            )
            
        if st.button("✅ Li e aceito os Termos de Uso", use_container_width=True):
            database.registrar_aceite(st.session_state.user["username"])
            st.session_state.user["aceitou_termos"] = True
            st.success("Termos aceitos com sucesso! Acessando o sistema...")
            time.sleep(1)
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
        perf = st.selectbox("Perfil", options=["USER", "ADMIN", "GESTOR"])
        ok    = st.form_submit_button("CRIAR", use_container_width=True)
    if ok:
        if not uname.strip() or not pw or not nome.strip():
            st.warning("Preencha todos os campos.")
        elif database.create_user(uname.strip(), pw, nome.strip(), perf, vbase):
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
        
        perfil_opts = ["USER", "ADMIN", "GESTOR"]
        current_perf = d.get("perfil", "USER")
        try: p_idx = perfil_opts.index(current_perf)
        except: p_idx = 0
        new_perf  = st.selectbox("Perfil", options=perfil_opts, index=p_idx)
        
        new_pw    = st.text_input("Nova Senha (em branco = manter)", type="password")
        c1, c2    = st.columns(2)
        salvar    = c1.form_submit_button("SALVAR",   use_container_width=True)
        cancelar  = c2.form_submit_button("CANCELAR", use_container_width=True)
    if salvar:
        if database.update_user(d["uid"], new_uname.strip(), new_nome.strip(),
                                new_perf, new_vbase, new_pw or None):
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
            if database.update_user(u["id"], new_uname, new_nome, u.get("perfil", "USER"), new_vbase, new_pw or None):
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

@st.dialog("Visualizar Detalhes do Registro")
def _dlg_visualizar_registro():
    cid = st.session_state.dlg_reg_ver
    row = database.get_chamado_by_id(cid)
    if not row:
        st.error("Registro não encontrado.")
        if st.button("FECHAR"):
            st.session_state.dlg_reg_ver = None
            st.rerun()
        return

    dt_obj = datetime.strptime(row[1], "%Y-%m-%d")
    data_fmt = dt_obj.strftime("%d/%m/%Y")
    dia_sem = utils.get_dia_semana(dt_obj)
    
    st.text_input("Data e Dia da Semana", value=f"{data_fmt} - {dia_sem.title()}", disabled=True)
    st.text_input("Hotel", value=f"{row[3]} - {row[4]}", disabled=True)
    
    c1, c2 = st.columns(2)
    c1.text_input("Início", value=row[5], disabled=True)
    c2.text_input("Término", value=row[6], disabled=True)
    
    st.text_input("Motivo", value=row[8] or "", disabled=True)
    st.text_area("Observações", value=row[7] or "", disabled=True)
    
    if st.button("FECHAR", use_container_width=True):
        st.session_state.dlg_reg_ver = None
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
        
        h_rows = get_cached_hoteis()
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
        f_motivo = st.text_input("Motivo", value=row[8] or "")
        f_obs    = st.text_area("Observações", value=row[7] or "")
        
        cb1, cb2 = st.columns(2)
        if cb1.form_submit_button("SALVAR", use_container_width=True):
            rid_, hnome_ = (f_hsel.split(" - ", 1) if f_hsel and " - " in f_hsel else ("", f_hsel))
            database.update_chamado(cid, f_data.strftime("%Y-%m-%d"), f_caso.strip(), rid_, hnome_, 
                                    utils.processar_input_horario(f_inicio), 
                                    utils.processar_input_horario(f_fim), f_obs.strip(), f_motivo.strip())
            st.cache_data.clear()  # Invalida cache para atualizar histórico imediatamente
            st.success("Atualizado!")
            st.session_state.dlg_reg_editar = None
            st.rerun()
        if cb2.form_submit_button("CANCELAR", use_container_width=True):
            st.session_state.dlg_reg_editar = None
            st.rerun()

@st.dialog("Confirmar Exclusão em Massa")
def _dlg_bulk_delete():
    sel_count = len(st.session_state.selected_records)
    st.warning(f"Tem certeza que deseja excluir {sel_count} registros selecionados? Esta ação não pode ser desfeita.")
    cols = st.columns(2)
    if cols[0].button("CANCELAR", use_container_width=True):
        st.session_state.dlg_bulk_delete = False
        st.rerun()
    if cols[1].button("SIM, EXCLUIR", type="primary", use_container_width=True):
        database.delete_chamados_bulk(list(st.session_state.selected_records))
        st.session_state.selected_records.clear()
        st.session_state.dlg_bulk_delete = False
        st.cache_data.clear()  # Invalida cache para atualizar histórico imediatamente
        st.success("Registros excluídos!")
        st.rerun()


@st.dialog("Confirmar Exclusão")
def _dlg_confirmar_delecao():
    cid = st.session_state.dlg_reg_deletar
    st.warning(f"Tem certeza que deseja excluir o registro ID {cid}?")
    c1, c2 = st.columns(2)
    if c1.button("SIM, EXCLUIR", use_container_width=True, type="primary"):
        database.delete_chamado(cid)
        st.session_state.dlg_reg_deletar = None
        st.cache_data.clear()  # Invalida cache para atualizar histórico imediatamente
        st.success("Removido!")
        st.rerun()
    if c2.button("NÃO", use_container_width=True):
        st.session_state.dlg_reg_deletar = None
        st.rerun()


# ── DISPARO DE MODAIS (Apenas um por execução) ────────────────────────────────
if st.session_state.dlg_hotel_novo:
    _dlg_novo_hotel()
elif st.session_state.dlg_hotel_editar is not None:
    _dlg_editar_hotel()
elif st.session_state.dlg_user_novo:
    _dlg_novo_usuario()
elif st.session_state.dlg_user_editar is not None:
    _dlg_editar_usuario()
elif st.session_state.dlg_perfil_editar:
    _dlg_editar_perfil()
elif st.session_state.dlg_reg_editar is not None:
    _dlg_editar_registro()
elif st.session_state.dlg_reg_deletar is not None:
    _dlg_confirmar_delecao()
elif st.session_state.dlg_reg_ver is not None:
    _dlg_visualizar_registro()
elif st.session_state.dlg_bulk_delete:
    _dlg_bulk_delete()


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
        cookie_manager.delete("auth_token")
        st.session_state.logged_in = False
        st.session_state.user      = None
        st.session_state.logout_lock = True # Trava o auto-login até a próxima ação manual
        st.rerun()

    st.markdown("---")
    st.markdown("### 📅 Relatório PDF")

    u_perfil = u.get("perfil", "USER").strip().upper()
    is_gestor = u_perfil == "GESTOR"
    is_admin  = u_perfil == "ADMIN"

    # Seleção de usuário para o PDF (Gestor/Admin podem escolher 'TODOS' ou um específico)
    target_user_name = u["nome"]
    target_username  = u["username"]
    target_vbase     = u.get("valor_base", 0.0)
    
    selected_target = "MEU RELATÓRIO"
    if u_perfil in ['ADMIN', 'GESTOR']:
        all_users = database.get_all_users()
        u_opts = ["Consolidado"] + [f"{usr[2]} ({usr[1]})" for usr in all_users]
        selected_target = st.selectbox("Colaborador", u_opts)
        
        if selected_target != "Consolidado":
            # Extrair username entre parênteses
            m = re.search(r"\((.*)\)", selected_target)
            if m:
                target_username = m.group(1)
                # Buscar nome e valor_base desse usuário
                for usr in all_users:
                    if usr[1] == target_username:
                        target_user_name = usr[2]
                        target_vbase = usr[5]
                        break

    MESES = ["JANEIRO","FEVEREIRO","MARÇO","ABRIL","MAIO","JUNHO",
             "JULHO","AGOSTO","SETEMBRO","OUTUBRO","NOVEMBRO","DEZEMBRO"]
    m_sel = st.selectbox("Mês Referente", MESES, index=mes_atual - 1)
    a_sel = st.number_input("Ano", 2024, 2030, ano_atual)

    if st.button("🚀 GERAR PDF", use_container_width=True):
        try:
            if selected_target == "Consolidado":
                # Lógica de PDF Consolidado
                rows_all = database.get_all_chamados(perfil=u_perfil, logged_username=u["username"])
                # Filtrar apenas o período desejado globalmente
                df_all = pd.DataFrame(rows_all, columns=["id","data","caso","pms","hotel","inicio","termino","observacoes", "motivo", "valor_base_snapshot", "username"])
                
                # Para o PDF consolidado, precisamos agrupar por usuário
                # Mas o utils.agrupar_por_data já faz o merge com datas do mês.
                # Teremos que adaptar o report_generator ou chamar múltiplas vezes?
                # O usuário pediu: "Cada plantonista deve começar em uma nova página"
                
                # Lista de tuplas (df_agrupado, nome_completo, valor_base)
                consolidados = []
                all_users_list = database.get_all_users()
                
                # Filtrar quem teve horas
                usernames_com_horas = df_all['username'].unique()
                
                for usr_tuple in all_users_list:
                    uname_ = usr_tuple[1]
                    if uname_ in usernames_com_horas:
                        df_u = df_all[df_all['username'] == uname_]
                        df_ag = utils.agrupar_por_data(df_u, m_sel, a_sel)
                        # Só adiciona se houver alguma hora trabalhada no período
                        if not df_ag[df_ag['horas_trabalhadas'] != ""].empty:
                            consolidados.append((df_ag, usr_tuple[2], usr_tuple[5]))

                if not consolidados:
                    st.warning("Nenhum registro encontrado para o período.")
                else:
                    path = f"relatorio_consolidado_{m_sel}_{a_sel}.pdf"
                    report_generator.gerar_pdf_massa(consolidados, m_sel, str(a_sel), path)
                    with open(path, "rb") as fh:
                        st.session_state["pdf_bytes"] = fh.read()
                    st.session_state["pdf_nome"] = path
                    if os.path.exists(path): os.remove(path)
                    st.success("✅ PDF Consolidado gerado!")
            else:
                # PDF Individual - Força o username do usuário se não for Admin/Gestor
                if u_perfil not in ['ADMIN', 'GESTOR']:
                    target_username = u["username"]
                rows = database.get_all_chamados(target_username, perfil=u_perfil, logged_username=u["username"])
                df = pd.DataFrame(rows, columns=["id","data","caso","pms","hotel","inicio","termino","observacoes", "motivo", "valor_base_snapshot", "username"])
                df_ag = utils.agrupar_por_data(df, m_sel, a_sel)
                path = f"folha_horas_{target_user_name.replace(' ', '_')}_{m_sel}_{a_sel}.pdf"
                report_generator.gerar_pdf(df_ag, target_user_name, m_sel, str(a_sel), target_vbase, path)
                with open(path, "rb") as fh:
                    st.session_state["pdf_bytes"] = fh.read()
                st.session_state["pdf_nome"] = path
                if os.path.exists(path): os.remove(path)
                st.success(f"✅ PDF de {target_user_name} gerado!")
                
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

    st.sidebar.markdown(
        """
        <div style='margin-top: 100px; line-height: 1.1;'>
            Desenvolvido por <b>Caique Novaes</b><br>
            Desenvolvido com <span style='font-size: 1.3rem;'>☕</span> e Python · 2026<br>
            <span style='color: #2ecc71; font-weight: bold;'>v1.3.0</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="page-title">CONTROLE DE HORAS EXTRAS</h1>', unsafe_allow_html=True)

# Hotéis carregados via cache para reduzir latência
h_rows = get_cached_hoteis()
h_opts = [f"{r} - {n}" for r, n in h_rows]

@st.fragment
def render_novo_registro_form():
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
            f_caso   = st.text_input("Caso / INC", key="reg_caso")
            f_hsel   = st.selectbox("Hotel", options=h_opts, index=None, placeholder="Selecione ou busque o hotel...", key="reg_hotel")
            f_motivo = st.text_input("Motivo *", placeholder="Descreva o motivo do chamado...", key="reg_motivo")
        with c2:
            f_inicio  = st.text_input("Início *",  placeholder="08:00", key="reg_inicio")
            f_fim     = st.text_input("Término *", placeholder="17:00", key="reg_termino")
            f_obs     = st.text_area("Observações", height=138, key="reg_obs")

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
                    vbase_atual = float(st.session_state.user.get("valor_base", 0.0))
                    database.save_chamado(
                        f_data.strftime("%Y-%m-%d"),
                        f_caso.strip() or None,
                        rid_, hnome_, ti, tf,
                        f_obs.strip() or None,
                        f_motivo.strip(),
                        st.session_state.user["username"],
                        vbase_atual
                    )
                    st.success(f"✅ Registrado!")
                    st.cache_data.clear()  # Invalida cache para atualizar histórico imediatamente
                    # Ativa o reset para a próxima execução (evita o erro de widget instanciado)
                    st.session_state.reg_reset = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

u_perfil = st.session_state.user.get("perfil", "USER").strip().upper()
is_admin = u_perfil == "ADMIN"
is_gestor = u_perfil == "GESTOR"

TABS_LIST = []
if not is_gestor:
    TABS_LIST.append("📝 Novo Registro")

TABS_LIST.append("📋 Histórico")
TABS_LIST.append("🏨 Hotéis")
TABS_LIST.append("⚙️ Usuários")

if is_admin:
    TABS_LIST.append("🔔 Aprovações")

tabs = st.tabs(TABS_LIST)
tab_map = dict(zip(TABS_LIST, tabs))

TAB_REG = tab_map.get("📝 Novo Registro")
TAB_HIST = tab_map.get("📋 Histórico")
TAB_HOTEL = tab_map.get("🏨 Hotéis")
TAB_USER = tab_map.get("⚙️ Usuários")
TAB_APROV = tab_map.get("🔔 Aprovações")


# ── ABA 0 – Novo Registro ─────────────────────────────────────────────────────
if TAB_REG:
    with TAB_REG:
        render_novo_registro_form()


# ── ABA 1 – Histórico ────────────────────────────────────────────────────────
with TAB_HIST:
    # Lógica de filtragem inicial: Se for USER, ele só vê o dele (Trava v1.2.1)
    username_filter = st.session_state.user["username"] if u_perfil == "USER" else None
    
    # Se for Admin ou Gestor, exibe o seletor de plantonista
    selected_usr_hist = "TODOS"
    if u_perfil in ['ADMIN', 'GESTOR']:
        all_usrs = database.get_all_users()
        u_opts_hist = ["TODOS"] + [f"{usr[2]} ({usr[1]})" for usr in all_usrs]
        selected_usr_hist = st.selectbox("Filtrar por Plantonista", u_opts_hist, key="hist_user_filter")
        
        if selected_usr_hist != "TODOS":
            m = re.search(r"\((.*)\)", selected_usr_hist)
            if m: username_filter = m.group(1)

    rows_all = get_cached_chamados(username_filter, u_perfil, st.session_state.user["username"])
    if rows_all:
        # Filtros de Histórico
        c_h1, c_h2 = st.columns(2)
        mes_atual_idx = mes_atual
        with c_h1:
            m_hist = st.selectbox("Mês", options=["TODOS", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], index=mes_atual_idx)
        with c_h2:
            a_hist = st.number_input("Ano ", min_value=2024, max_value=2050, value=ano_atual, step=1)
        
        # Lógica de Filtragem no Histórico (Ciclo de Competência)
        if m_hist != "TODOS":
            inicio_comp, fim_comp = utils.obter_faixa_periodo(m_hist, a_hist)
            st.caption(f"Exibindo período de competência: **{inicio_comp.strftime('%d/%m/%Y')}** a **{fim_comp.strftime('%d/%m/%Y')}**")

        rows = []
        for r in rows_all:
            dt_obj = datetime.strptime(r[1], "%Y-%m-%d")
            if m_hist != "TODOS":
                if not (inicio_comp <= dt_obj <= fim_comp): continue
            else:
                if a_hist and dt_obj.year != a_hist: continue
            rows.append(r)
            
        if rows:
            sel_count = len(st.session_state.selected_records)
            cols_bulk = st.columns([2, 6])
            with cols_bulk[0]:
                if not is_gestor:
                    if st.button(f"🗑️ Deletar {sel_count} selecionado(s)" if sel_count > 0 else "Deletar Selecionados", disabled=(sel_count == 0), use_container_width=True):
                        st.session_state.dlg_bulk_delete = True
                        st.rerun()
                
            cols_h = st.columns([0.4, 0.8, 0.8, 1.5, 1.2, 0.7, 0.7, 1.2, 0.8])
            headers = ["", "Data", "Caso", "Hotel", "Motivo", "Início", "Término", "Observações", "Ações"]
            for col, h in zip(cols_h, headers):
                col.markdown(f"**{h}**")
            st.divider()
            
            def bind_checkbox(r_id):
                key = f"chk_{r_id}"
                if st.session_state[key]: st.session_state.selected_records.add(r_id)
                else: st.session_state.selected_records.discard(r_id)
            
            for r in rows:
                c0, c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([0.4, 0.8, 0.8, 1.5, 1.2, 0.7, 0.7, 1.2, 0.8])
                rid = r[0]
                
                # Checkbox sync (Gestor não seleciona pois não deleta em massa)
                chk_key = f"chk_{rid}"
                if not is_gestor:
                    c0.checkbox(" ", key=chk_key, value=(rid in st.session_state.selected_records), on_change=bind_checkbox, args=(rid,), label_visibility="collapsed")
                
                dt_fmt = datetime.strptime(r[1], "%Y-%m-%d").strftime("%d/%m/%Y")
                c1.write(dt_fmt)
                c2.write(r[2] or "—")
                c3.write(f"{r[3]} - {r[4]}")
                c4.write(r[8] or "—")
                c5.write(r[5])
                c6.write(r[6])
                c7.write(r[7] or "—")
                
                if is_gestor:
                    # Gestor: Apenas ícone de Olho
                    if c8.button("👁️", key=f"ver_reg_{r[0]}", help="Visualizar", use_container_width=True):
                        st.session_state.dlg_reg_ver = r[0]
                        st.rerun()
                else:
                    bt_ver, bt_ed = c8.columns(2)
                    if bt_ver.button("👁️", key=f"ver_reg_{r[0]}"):
                        st.session_state.dlg_reg_ver = r[0]
                        st.rerun()
                    if bt_ed.button("✏️", key=f"ed_reg_{r[0]}"):
                        st.session_state.dlg_reg_editar = r[0]
                        st.rerun()
    else:
        st.info("Nenhum registro encontrado.")


# ── ABA 2 – Hotéis ───────────────────────────────────────────────────────────
with TAB_HOTEL:
    st.subheader("Gestão de Hotéis")
    if not is_gestor:
        if st.button("➕ Sugerir Novo Hotel", type="primary"):
            st.session_state.dlg_hotel_novo = True
            st.rerun()

    if h_rows:
        if is_gestor:
            c_cod, c_nom = st.columns([1.5, 6])
            c_cod.markdown("**RID**"); c_nom.markdown("**Nome**")
        else:
            c_cod, c_nom, c_ed, c_del = st.columns([1.2, 5, 0.6, 0.6])
            c_cod.markdown("**RID**"); c_nom.markdown("**Nome**")
            
        st.divider()
        for i, (r, n) in enumerate(h_rows):
            if is_gestor:
                ca, cb = st.columns([1.5, 6])
                ca.write(r); cb.write(n)
            else:
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
with TAB_USER:
    if is_admin or is_gestor:
        st.subheader("Gestão de Usuários")
        if is_admin:
            if st.button("➕ Novo Usuário", type="primary"):
                st.session_state.dlg_user_novo = True
                st.rerun()

        u_list = database.get_all_users()
        if u_list:
            st.divider()
            for usr in u_list:
                # usr: id, username, nome_completo, is_admin, must_change_password, valor_base, perfil
                uid, uname, unom, uadm, umust, uvb, uperfil_ = usr
                if is_gestor:
                    cu, cn, cp = st.columns([2, 4, 1.5])
                    cu.write(f"**{uname}**")
                    cn.write(unom or "—")
                    cp.write(f"🏷️ {uperfil_}")
                else:
                    cu, cn, cp, ce, cr, cx = st.columns([1.5, 2.5, 1, 0.6, 0.6, 0.6])
                    cu.write(f"**{uname}**")
                    cn.write(unom or "—")
                    cp.write("🔴 Admin" if uperfil_ == "ADMIN" else ("🟡 Gestor" if uperfil_ == "GESTOR" else "🟢 User"))
                    if ce.button("✏️", key=f"edu_{uid}", help="Editar"):
                        st.session_state.dlg_user_editar = {
                            "uid": uid, "user": uname, "nome": unom, "admin": uadm, "valor_base": uvb, "perfil": uperfil_
                        }
                        st.rerun()
                    if cr.button("🔑", key=f"resetu_{uid}", help="Resetar Senha"):
                        database.reset_password_admin(uid)
                        st.success(f"Senha de {uname} resetada!")
                    if cx.button("🗑️", key=f"dlu_{uid}", help="Excluir"):
                        database.delete_user(uid)
                        st.rerun()
    else:
        st.info("Acesso restrito.")

if is_admin and TAB_APROV:
    with TAB_APROV:
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
                    st.cache_data.clear() # Limpa o cache para atualizar lista de hotéis
                    st.rerun()
                if bt_rj.button("❌", key=f"rj_{sid}"):
                    database.processar_solicitacao(sid, False)
                    st.rerun()
        else:
            st.info("Nenhuma solicitação pendente.")
