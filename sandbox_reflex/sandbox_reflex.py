import reflex as rx
from . import login
from .state import AuthState
from .data_state import DataState, MESES_PT, ANOS
from .state_form import FormState
from .state_hoteis import HotelState
from .state_usuarios import UsuarioState

def lgpd_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Termos de Uso e LGPD"),
            rx.box(
                rx.text(
                    "Para continuar utilizando o Controle de Horas Extras, você deve aceitar nossa ",
                    rx.text(
                        "política de tratamento",
                        as_="span",
                        weight="bold",
                        color=rx.color("blue", 11),
                        style={"cursor": "pointer", "textDecoration": "underline"},
                        on_click=AuthState.toggle_policy,
                    ),
                    " de dados de acordo com a LGPD.",
                    size="2",
                    margin_bottom="16px",
                ),
                rx.cond(
                    AuthState.show_policy,
                    rx.box(
                        rx.text(
                            "1. Coleta: Coletamos dados de identificação (nome, usuário) e informações de jornada de trabalho.\n"
                            "2. Finalidade: Os dados são utilizados estritamente para o cálculo e controle de horas extras.\n"
                            "3. Segurança: Seus dados financeiros e senhas são criptografados em trânsito e em repouso.\n"
                            "4. Direitos do Titular: Você pode solicitar revisão ou exclusão de seus dados conforme as diretrizes da Lei Geral de Proteção de Dados (LGPD).",
                            size="1",
                            color="gray",
                            white_space="pre-wrap"
                        ),
                        padding="12px",
                        background_color=rx.color("gray", 2),
                        border_radius="md",
                        margin_bottom="16px",
                        border=f"1px solid {rx.color('gray', 4)}",
                    )
                ),
            ),
            rx.flex(
                rx.button(
                        "Concordo e Aceito",
                        on_click=AuthState.aceitar_termos_lgpd,
                        color_scheme="ruby",
                        width="100%",
                        cursor="pointer",
                    ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            on_pointer_down_outside=rx.prevent_default,
            on_escape_key_down=rx.prevent_default,
        ),
        open=AuthState.needs_lgpd_acceptance,
    )

def novo_chamado_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    FormState.record_id == -1,
                    "Inserir Novo Chamado",
                    rx.cond(FormState.is_view_only, "Visualizar Chamado", "Editar Chamado")
                )
            ),
            rx.box(
                rx.cond(
                    FormState.error_message != "",
                    rx.callout(
                        FormState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        margin_bottom="1em",
                    )
                ),
                rx.grid(
                    # Coluna 1
                    rx.vstack(
                        rx.text("Data do Atendimento", size="2", font_weight="bold"),
                        rx.input(type="date", value=FormState.f_data, on_change=FormState.set_f_data, disabled=FormState.is_view_only, width="100%"),
                        
                        rx.text("Caso / INC", size="2", font_weight="bold"),
                        rx.input(placeholder="Caso...", value=FormState.f_caso, on_change=FormState.set_f_caso, disabled=FormState.is_view_only, width="100%"),
                        
                        rx.text("Hotel", size="2", font_weight="bold"),
                        rx.box(
                            rx.el.datalist(
                                rx.foreach(FormState.hoteis_opts, lambda h: rx.el.option(value=h)),
                                id="hoteis_list"
                            ),
                            rx.input(
                                placeholder="Selecione ou busque o hotel...",
                                value=FormState.f_hotel,
                                on_change=FormState.set_f_hotel,
                                disabled=FormState.is_view_only,
                                custom_attrs={"list": "hoteis_list"},
                                width="100%",
                                background_color="#262730",
                                border="1px solid rgba(250, 250, 250, 0.2)",
                                color="white",
                                _focus={"border": "1px solid #ff4d4d", "box_shadow": "0 0 0 1px #ff4d4d"},
                                cursor="pointer",
                            ),
                            width="100%"
                        ),
                        
                        rx.text("Motivo *", size="2", font_weight="bold"),
                        rx.input(placeholder="Descreva o motivo do chamado...", value=FormState.f_motivo, on_change=FormState.set_f_motivo, disabled=FormState.is_view_only, width="100%"),
                        width="100%",
                        spacing="2",
                    ),
                    # Coluna 2
                    rx.vstack(
                        rx.text("Início *", size="2", font_weight="bold"),
                        rx.input(placeholder="08:00", value=FormState.f_inicio, on_change=FormState.set_f_inicio, disabled=FormState.is_view_only, width="100%"),
                        
                        rx.text("Término *", size="2", font_weight="bold"),
                        rx.input(placeholder="17:00", value=FormState.f_termino, on_change=FormState.set_f_termino, disabled=FormState.is_view_only, width="100%"),
                        
                        rx.text("Observações", size="2", font_weight="bold"),
                        rx.text_area(placeholder="Observações...", value=FormState.f_obs, on_change=FormState.set_f_obs, disabled=FormState.is_view_only, height="138px", width="100%"),
                        width="100%",
                        spacing="2",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
            ),
            rx.flex(
                rx.button(
                    "Cancelar",
                    color_scheme="gray",
                    variant="soft",
                    on_click=FormState.close_modal,
                    cursor="pointer",
                ),
                rx.cond(
                    ~FormState.is_view_only,
                    rx.button(
                        "💾 SALVAR",
                        on_click=FormState.save_record,
                        background_color="#800000",
                        color="white",
                        cursor="pointer",
                        _hover={"background_color": "#A30000"},
                    )
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": "600px"},
        ),
        open=FormState.is_modal_open,
    )

def novo_hotel_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(HotelState.h_original_rid == "", "Novo Hotel", "Editar Hotel"), 
                color="#fafafa"
            ),
            rx.dialog.description("Preencha os dados do hotel abaixo.", color="#b0b0b8"),
            rx.vstack(
                rx.text("RID do Hotel *", size="2", font_weight="bold"),
                rx.input(
                    placeholder="Ex: ABCDE", 
                    value=HotelState.h_rid, 
                    on_change=HotelState.set_h_rid,
                    width="100%"
                ),
                
                rx.text("Nome do Hotel *", size="2", font_weight="bold"),
                rx.input(placeholder="Nome...", value=HotelState.h_nome, on_change=HotelState.set_h_nome, width="100%"),
                spacing="2",
                width="100%",
                margin_top="1em"
            ),
            rx.flex(
                rx.button("Cancelar", color_scheme="gray", variant="soft", on_click=HotelState.close_modal, cursor="pointer"),
                rx.button(
                    "💾 SALVAR",
                    on_click=HotelState.save_hotel,
                    background_color="#800000",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#A30000"},
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": "450px"},
        ),
        open=HotelState.is_modal_open,
    )

def novo_usuario_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(UsuarioState.u_id == -1, "Novo Usuário", "Editar Usuário"), 
                color="#fafafa"
            ),
            rx.dialog.description("Preencha os dados do usuário abaixo.", color="#b0b0b8"),
            rx.vstack(
                rx.text("Username (Login) *", size="2", font_weight="bold"),
                rx.input(placeholder="johndoe", value=UsuarioState.u_username, on_change=UsuarioState.set_u_username, width="100%"),
                
                rx.text("Nome Completo *", size="2", font_weight="bold"),
                rx.input(placeholder="John Doe", value=UsuarioState.u_nome, on_change=UsuarioState.set_u_nome, width="100%"),
                
                rx.text("Perfil *", size="2", font_weight="bold"),
                rx.select(
                    ["USER", "GESTOR", "ADMIN"],
                    value=UsuarioState.u_perfil,
                    on_change=UsuarioState.set_u_perfil,
                    width="100%"
                ),
                
                rx.cond(
                    UsuarioState.u_id == -1,
                    rx.text("Senha padrão ao criar: mudar@123", color="#f39c12", size="2", margin_top="1em"),
                    rx.box()
                ),
                
                spacing="2",
                width="100%",
                margin_top="1em"
            ),
            rx.flex(
                rx.button("Cancelar", color_scheme="gray", variant="soft", on_click=UsuarioState.close_modal, cursor="pointer"),
                rx.button(
                    "💾 SALVAR",
                    on_click=UsuarioState.save_usuario,
                    background_color="#800000",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#A30000"},
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": "450px"},
        ),
        open=UsuarioState.is_modal_open,
    )

def perfil_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("👤 Meu Perfil", color="#fafafa"),
            rx.dialog.description("Atualize suas informações pessoais.", color="#b0b0b8"),
            rx.vstack(
                rx.text("Nome Completo", size="2", font_weight="bold"),
                rx.input(placeholder="Seu nome...", value=AuthState.p_nome, on_change=AuthState.set_p_nome, width="100%"),
                
                rx.cond(
                    AuthState.user_info["perfil"] != "GESTOR",
                    rx.box(
                        rx.text("Novo Valor Base (R$/h)", size="2", font_weight="bold", margin_top="1em"),
                        rx.text("Seu valor atual que será usado para calcular os ganhos do mês.", color="#888", size="1", margin_top="-10px"),
                        rx.input(placeholder="Ex: 15.50", value=AuthState.p_valor_base, on_change=AuthState.set_p_valor_base, width="100%"),
                        width="100%"
                    ),
                    rx.box()
                ),
                
                rx.text("Nova Senha", size="2", font_weight="bold", margin_top="1em"),
                rx.text("Deixe em branco se não quiser alterar a senha atual.", color="#888", size="1", margin_top="-10px"),
                rx.input(type="password", placeholder="Digite a nova senha...", value=AuthState.p_new_password, on_change=AuthState.set_p_new_password, width="100%"),
                
                spacing="2",
                width="100%",
                margin_top="1em"
            ),
            rx.flex(
                rx.button("Cancelar", color_scheme="gray", variant="soft", on_click=AuthState.close_profile, cursor="pointer"),
                rx.button(
                    "💾 SALVAR",
                    on_click=AuthState.save_profile,
                    background_color="#800000",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#A30000"},
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": "400px"},
        ),
        open=AuthState.is_profile_modal_open,
    )

def kpi_card(title: str, value: str, emoji: str) -> rx.Component:
    # Cópia exata do CSS do Streamlit
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(emoji, font_size="0.9rem"),
                rx.text(
                    title.upper(), 
                    font_size="0.8rem", 
                    color="#b0b0b8", 
                    font_weight="600", 
                    letter_spacing="0.05em"
                ),
                spacing="2",
                align="center",
            ),
            rx.text(
                value, 
                font_size="1.45rem", 
                font_weight="700", 
                color="#ff4d4d", 
                text_align="center",
                margin_top="4px"
            ),
            spacing="1",
            align="center",
            width="100%",
        ),
        width="100%",
        border="1px solid #800000",
        border_radius="12px",
        padding="12px 16px",
        background_color="transparent",
        box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "transform": "translateY(-3px)",
            "background_color": "rgba(128, 0, 0, 0.05)",
            "box_shadow": "0 8px 20px rgba(128, 0, 0, 0.3)",
            "border_color": "#ff4d4d",
        }
    )

def historico_tab() -> rx.Component:
    return rx.vstack(
        # Filtros Mês / Ano alinhados estilo colunas Streamlit
        rx.hstack(
            rx.vstack(
                rx.text("Mês", font_size="14px", color="#fafafa", margin_bottom="-8px"),
                rx.select(
                    MESES_PT,
                    value=DataState.mes_ref,
                    on_change=DataState.set_mes_ref,
                    width="200px",
                    color_scheme="ruby",
                    variant="surface",
                    cursor="pointer",
                ),
            ),
            rx.vstack(
                rx.text("Ano", font_size="14px", color="#fafafa", margin_bottom="-8px"),
                rx.select(
                    ANOS,
                    value=DataState.ano_ref,
                    on_change=DataState.set_ano_ref,
                    width="120px",
                    color_scheme="ruby",
                    variant="surface",
                    cursor="pointer",
                ),
            ),
            rx.cond(
                AuthState.user_info["perfil"] != "USER",
                rx.vstack(
                    rx.text("Plantonista", font_size="14px", color="#fafafa", margin_bottom="-8px"),
                    rx.select(
                        DataState.opcoes_plantonistas,
                        value=DataState.filtro_plantonista,
                        on_change=DataState.set_filtro_plantonista,
                        width="200px",
                        placeholder="Plantonista",
                        color_scheme="ruby",
                        variant="surface",
                        cursor="pointer",
                    ),
                ),
                rx.box()
            ),
            spacing="4",
            margin_bottom="1.5em",
        ),
        
        # 4 KPI Cards (Ordem e design exatos)
        rx.grid(
            kpi_card("Horas (50% / 100%)", DataState.total_horas_50 + " / " + DataState.total_horas_100, "🕐"),
            kpi_card("Ganhos Estimados", DataState.ganhos_estimados, "💰"),
            kpi_card("Total Chamados", DataState.total_chamados.to_string(), "📋"),
            kpi_card("Média / Chamado", DataState.media_por_chamado, "📊"),
            columns="4",
            spacing="4",
            width="100%",
            margin_bottom="2em",
        ),
        
        # Botões de Ação na Tabela (Bulk Delete)
        rx.cond(
            AuthState.user_info["perfil"] != "GESTOR",
            rx.hstack(
                rx.cond(
                    DataState.selected_records.length() > 0,
                    rx.button(
                        "🗑️ Deletar selecionados",
                        on_click=DataState.bulk_delete,
                        background_color="#800000",
                        color="white",
                        cursor="pointer",
                        _hover={"background_color": "#A30000"},
                        margin_bottom="1em",
                    ),
                    rx.button(
                        "Deletar Selecionados",
                        disabled=True,
                        background_color="rgba(128,0,0,0.2)",
                        color="#888",
                        margin_bottom="1em",
                    )
                ),
                spacing="4",
            ),
            rx.box()
        ),

        # Tabela de Registros - Header igual Streamlit
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        rx.cond(
                            AuthState.user_info["perfil"] != "GESTOR",
                            rx.checkbox(
                                checked=DataState.is_all_selected,
                                on_change=DataState.toggle_select_all
                            ),
                            rx.box()
                        )
                    ),
                    rx.table.column_header_cell("Data"),
                    rx.table.column_header_cell("Caso"),
                    rx.table.column_header_cell("Hotel"),
                    rx.table.column_header_cell("Motivo"),
                    rx.table.column_header_cell("Início"),
                    rx.table.column_header_cell("Término"),
                    rx.table.column_header_cell("Observações"),
                    rx.table.column_header_cell("Ações"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    DataState.registros_agrupados,
                    lambda row: rx.table.row(
                        rx.table.cell(
                            rx.cond(
                                AuthState.user_info["perfil"] != "GESTOR",
                                rx.checkbox(
                                    on_change=lambda checked: DataState.toggle_record(row["id"], checked),
                                    checked=DataState.selected_records.contains(row["id"])
                                ),
                                rx.box()
                            )
                        ),
                        rx.table.cell(row["data"]),
                        rx.table.cell(row["caso"]),
                        rx.table.cell(row["hotel"]),
                        rx.table.cell(row["motivo"]),
                        rx.table.cell(row["inicio"]),
                        rx.table.cell(row["termino"]),
                        rx.table.cell(row["observacoes"]),
                        rx.table.cell(
                            rx.hstack(
                                rx.button("👁️", on_click=lambda: FormState.open_view_record(row["id"]), variant="ghost", font_size="1rem", cursor="pointer"),
                                rx.cond(
                                    AuthState.user_info["perfil"] != "GESTOR",
                                    rx.button("✏️", on_click=lambda: FormState.open_edit_record(row["id"]), variant="ghost", font_size="1rem", cursor="pointer"),
                                    rx.box()
                                ),
                                spacing="4"
                            )
                        ),
                    )
                )
            ),
            width="100%",
            variant="surface",
            size="2",
        ),
        width="100%",
    )

def hoteis_tab() -> rx.Component:
    return rx.vstack(
        # Barra de Pesquisa e Botão Novo
        rx.hstack(
            rx.input(
                placeholder="🔍 Buscar por RID ou Nome...",
                value=HotelState.search_query,
                on_change=HotelState.set_search_query,
                width="300px",
                background_color="#262730",
                border="1px solid rgba(250, 250, 250, 0.2)",
                color="white",
                _focus={"border": "1px solid #ff4d4d", "box_shadow": "0 0 0 1px #ff4d4d"},
            ),
            rx.spacer(),
            rx.cond(
                AuthState.user_info["perfil"] != "GESTOR",
                rx.button(
                    "🏨 Novo Hotel",
                    on_click=HotelState.open_new_hotel,
                    background_color="#2ecc71",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#27ae60"},
                ),
                rx.box()
            ),
            width="100%",
            margin_top="1em",
            margin_bottom="0",
        ),
        
        # Tabela de Hotéis
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("RID"),
                    rx.table.column_header_cell("Nome do Hotel"),
                    rx.table.column_header_cell("Status", width="100px", text_align="center"),
                    rx.table.column_header_cell("Ações", width="150px", text_align="right"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    HotelState.filtered_hoteis,
                    lambda h: rx.table.row(
                        rx.table.cell(rx.text(h["rid"], weight="bold")),
                        rx.table.cell(h["nome"]),
                        rx.table.cell(
                            rx.cond(
                                h["has_pendency"],
                                rx.tooltip(
                                    rx.icon(tag="triangle_alert", color="#f39c12", size=20),
                                    content=f"{h['pendencia_tipo']} Pendente",
                                ),
                                rx.text("-", color="#666")
                            ),
                            align="center"
                        ),
                        rx.table.cell(
                            rx.cond(
                                AuthState.user_info["perfil"] != "GESTOR",
                                rx.hstack(
                                    rx.button("✏️", on_click=lambda: HotelState.open_edit_hotel(h["rid"], h["nome"]), variant="ghost", cursor="pointer", disabled=h["has_pendency"]),
                                    rx.button("🗑️", on_click=lambda: HotelState.delete_hotel(h["rid"], h["nome"]), variant="ghost", cursor="pointer", disabled=h["has_pendency"]),
                                    spacing="2",
                                    justify="end"
                                ),
                                rx.box()
                            ),
                            align="right"
                        ),
                    )
                )
            ),
            width="100%",
            variant="surface",
            size="2",
        ),
        
        # Painel de Aprovações para ADMIN
        rx.cond(
            rx.cond(HotelState.solicitacoes.length() > 0, True, False) & (AuthState.user_info["perfil"] == "ADMIN"),
            rx.vstack(
                rx.heading("Aprovações Pendentes", size="3", color="#f39c12", margin_top="2em", margin_bottom="1em"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Tipo"),
                            rx.table.column_header_cell("RID"),
                            rx.table.column_header_cell("Novo Nome"),
                            rx.table.column_header_cell("Solicitante ID"),
                            rx.table.column_header_cell("Ação", text_align="right"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            HotelState.solicitacoes,
                            lambda s: rx.table.row(
                                rx.table.cell(rx.badge(s["tipo"], color_scheme="orange")),
                                rx.table.cell(s["rid"]),
                                rx.table.cell(s["nome"]),
                                rx.table.cell(s["user_id"]),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button("✅", on_click=lambda: HotelState.approve_solicitacao(s["id"]), variant="ghost", cursor="pointer"),
                                        rx.button("❌", on_click=lambda: HotelState.reject_solicitacao(s["id"]), variant="ghost", cursor="pointer"),
                                        spacing="2",
                                        justify="end"
                                    ),
                                    align="right"
                                ),
                            )
                        )
                    ),
                    width="100%",
                    variant="surface",
                ),
                width="100%"
            )
        ),
        width="100%",
    )

def aprovacoes_tab() -> rx.Component:
    return rx.cond(
        AuthState.user_info["perfil"] == "ADMIN",
        rx.vstack(
            rx.heading("Aprovações Pendentes", size="4", color="#fafafa", margin_top="1em", margin_bottom="1em"),
            rx.cond(
                HotelState.solicitacoes.length() > 0,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Ação"),
                            rx.table.column_header_cell("RID Alvo"),
                            rx.table.column_header_cell("Nome Proposto"),
                            rx.table.column_header_cell("Opções"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            HotelState.solicitacoes,
                            lambda req: rx.table.row(
                                rx.table.cell(rx.badge(req["tipo"], color_scheme=rx.cond(req["tipo"]=="EDIT", "yellow", "red"))),
                                rx.table.cell(req["rid"]),
                                rx.table.cell(req["nome"]),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button("✅", on_click=lambda: HotelState.approve_solicitacao(req["id"]), variant="ghost", cursor="pointer", color="green"),
                                        rx.button("❌", on_click=lambda: HotelState.reject_solicitacao(req["id"]), variant="ghost", cursor="pointer", color="red"),
                                        spacing="2"
                                    )
                                )
                            )
                        )
                    ),
                    width="100%",
                    variant="surface",
                    size="2",
                ),
                rx.text("Nenhuma solicitação pendente no momento.", color="#b0b0b8")
            ),
            width="100%",
        ),
        rx.box()
    )

def usuarios_tab() -> rx.Component:
    return rx.cond(
        AuthState.user_info["perfil"] == "ADMIN",
        rx.vstack(
            rx.hstack(
                rx.heading("Controle de Usuários", size="4", color="#fafafa"),
                rx.spacer(),
                rx.button(
                    "👤 Novo Usuário",
                    on_click=UsuarioState.open_new_user,
                    background_color="#2ecc71",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#27ae60"},
                ),
                width="100%",
                margin_top="1em",
                margin_bottom="0",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Username"),
                        rx.table.column_header_cell("Nome Completo"),
                        rx.table.column_header_cell("Perfil", text_align="center"),
                        rx.table.column_header_cell("Ações", text_align="right"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        UsuarioState.usuarios,
                        lambda u: rx.table.row(
                            rx.table.cell(rx.text(u["username"], weight="bold")),
                            rx.table.cell(u["nome_completo"]),
                            rx.table.cell(
                                rx.badge(u["perfil"], color_scheme=rx.cond(u["perfil"] == "ADMIN", "ruby", "blue")),
                                align="center"
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.tooltip(
                                        rx.button("🔑", on_click=lambda: UsuarioState.reset_password(u["id"]), variant="ghost", cursor="pointer"),
                                        content="Resetar Senha (mudar@123)"
                                    ),
                                    rx.tooltip(
                                        rx.button("✏️", on_click=lambda: UsuarioState.open_edit_user(u), variant="ghost", cursor="pointer"),
                                        content="Editar Usuário"
                                    ),
                                    rx.tooltip(
                                        rx.button("🗑️", on_click=lambda: UsuarioState.delete_usuario(u["id"]), variant="ghost", cursor="pointer"),
                                        content="Excluir Usuário"
                                    ),
                                    spacing="2",
                                    justify="end"
                                ),
                                align="right"
                            ),
                        )
                    )
                ),
                width="100%",
                variant="surface",
                size="2",
            ),
            width="100%"
        ),
        rx.vstack(
            rx.icon(tag="shield_alert", size=48, color="#e74c3c"),
            rx.heading("Acesso Restrito", size="5", color="#e74c3c"),
            rx.text("Apenas Administradores podem visualizar esta página.", color="#b0b0b8"),
            align="center",
            margin_top="3em",
            width="100%"
        )
    )

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading(f"👤 {AuthState.user_info['nome']}", size="4", color="#fafafa", text_align="center", width="100%", margin_bottom="0"),
        rx.text(f"@{AuthState.user_info['username']}", size="2", color="#b0b0b8", margin_top="-10px", margin_bottom="1em", text_align="center", width="100%"),
        rx.hstack(
            rx.button("Meu Perfil", on_click=AuthState.open_profile, variant="outline", color="#fafafa", border="1px solid #444", width="50%", cursor="pointer", _hover={"background_color": "rgba(255,255,255,0.1)"}),
            rx.button("Sair", on_click=AuthState.logout, background_color="transparent", color="#fafafa", border="1px solid #444", width="50%", cursor="pointer", _hover={"background_color": "rgba(255,255,255,0.1)"}),
            width="100%",
            spacing="2"
        ),
        rx.divider(margin_y="2em", border_color="#333"),
        
        rx.heading("📅 Relatórios", size="3", color="#fafafa", margin_bottom="0.5em"),
        rx.button(
            rx.cond(DataState.is_generating_pdf, "Gerando...", "Baixar Relatório"),
            on_click=DataState.baixar_pdf_individual,
            disabled=DataState.is_generating_pdf,
            background_color="#800000",
            color="white",
            width="100%",
            margin_bottom="0.5em",
            cursor="pointer",
            _hover={"background_color": "#A30000"},
        ),
        rx.cond(
            AuthState.user_info["perfil"] != "USER",
            rx.button(
                rx.cond(DataState.is_generating_pdf, "Processando Equipe...", "Baixar Consolidado"),
                on_click=DataState.baixar_pdf_equipe,
                disabled=DataState.is_generating_pdf,
                variant="outline",
                color_scheme="ruby",
                width="100%",
                cursor="pointer",
            )
        ),
        
        rx.spacer(),
        rx.vstack(
            rx.text(
                "Desenvolvido por ",
                rx.text("Caique Novaes", as_="span", weight="bold"),
            ),
            rx.text("Desenvolvido com ☕ e Python · 2026", margin_top="4px", white_space="nowrap"),
            rx.text("v2.0", color="#2ecc71", weight="bold"),
            font_size="10px",
            color="#b0b0b8",
            align="center",
            spacing="1",
            width="100%",
            line_height="1.2",
            font_family="'Montserrat', sans-serif"
        ),
        width="300px",
        height="100vh",
        padding="1.5em",
        background_color="#1c1c1c", # Streamlit sidebar escuro original
        border_right="1px solid #333",
        position="sticky",
        top="0",
    )

def plantonista_alert_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon(tag="triangle_alert", color="#f39c12", size=24),
                    rx.text("Atenção", color="#fafafa"),
                    spacing="2",
                    align_items="center",
                    justify="center"
                )
            ),
            rx.dialog.description(
                "Por favor, selecione um plantonista específico no filtro da tabela para baixar o relatório individual.", 
                color="#b0b0b8", 
                margin_top="1em",
                text_align="center"
            ),
            rx.flex(
                rx.button(
                    "Entendi",
                    on_click=DataState.close_plantonista_alert,
                    background_color="#800000",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#A30000"},
                ),
                justify="center",
                margin_top="2em",
            ),
            style={"max_width": "400px"},
        ),
        open=DataState.show_plantonista_alert,
    )

def empty_equipe_alert_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon(tag="triangle_alert", color="#f39c12", size=24),
                    rx.text("Atenção", color="#fafafa"),
                    spacing="2",
                    align_items="center",
                    justify="center"
                )
            ),
            rx.dialog.description(
                "Não há registros de nenhum colaborador para gerar o relatório consolidado neste período.", 
                color="#b0b0b8", 
                margin_top="1em",
                text_align="center"
            ),
            rx.flex(
                rx.button(
                    "Entendi",
                    on_click=DataState.close_empty_equipe_alert,
                    background_color="#800000",
                    color="white",
                    cursor="pointer",
                    _hover={"background_color": "#A30000"},
                ),
                justify="center",
                margin_top="2em",
            ),
            style={"max_width": "400px"},
        ),
        open=DataState.show_empty_equipe_alert,
    )

@rx.page(route="/", title="Home | Horas Extras", on_load=[AuthState.check_session, DataState.load_defaults, HotelState.load_hoteis, UsuarioState.load_usuarios])
def index() -> rx.Component:
    return rx.hstack(
        empty_equipe_alert_modal(),
        plantonista_alert_modal(),
        lgpd_modal(),
        perfil_modal(),
        novo_chamado_modal(),
        novo_hotel_modal(),
        novo_usuario_modal(),
        sidebar(),
        rx.vstack(
            rx.heading(
                "CONTROLE DE HORAS EXTRAS", 
                font_size="1.35rem", 
                font_weight="700",
                letter_spacing=".04em",
                color="#800000",
                text_align="center",
                width="100%",
                padding_bottom="10px",
                margin_bottom="20px",
                margin_top="10px",
                border_bottom="2px solid #800000"
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("📋 Histórico", value="historico", cursor="pointer"),
                    rx.cond(
                        AuthState.user_info["perfil"] != "GESTOR",
                        rx.tabs.trigger("📝 Novo Registro", value="novo", cursor="pointer"),
                        rx.box()
                    ),
                    rx.tabs.trigger("🏨 Hotéis", value="hoteis", cursor="pointer"),
                    rx.cond(
                        AuthState.user_info["perfil"] == "ADMIN",
                        rx.tabs.trigger("⚙️ Usuários", value="usuarios", cursor="pointer"),
                        rx.box()
                    ),
                    rx.cond(
                        AuthState.user_info["perfil"] == "ADMIN",
                        rx.tabs.trigger("🔔 Aprovações", value="aprovacoes", cursor="pointer"),
                        rx.box()
                    ),
                ),
                rx.tabs.content(
                    historico_tab(),
                    value="historico",
                    padding_top="1em"
                ),
                rx.tabs.content(
                    rx.box(),
                    value="novo",
                ),
                rx.tabs.content(
                    hoteis_tab(),
                    value="hoteis",
                ),
                rx.tabs.content(
                    aprovacoes_tab(),
                    value="aprovacoes",
                ),
                rx.tabs.content(
                    usuarios_tab(),
                    value="usuarios",
                ),
                value=DataState.active_tab,
                on_change=DataState.set_active_tab,
                width="100%",
            ),
            width="100%",
            padding="2em",
            height="100vh",
            overflow_y="auto",
        ),
        width="100%",
        align_items="flex-start",
        background_color="#0e1117", # Streamlit Dark Mode background
    )

# Configuração Global
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=False,
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap"
    ],
    style={
        "font_family": "'Inter', sans-serif",
    }
)
