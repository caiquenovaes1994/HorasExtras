import reflex as rx

def changelog_row(versao: str, data: str, descricao: str) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text(versao, weight="bold", color="#2ecc71")),
        rx.table.cell(data),
        rx.table.cell(descricao),
    )

@rx.page(route="/changelog", title="Histórico de Versões | Horas Extras")
def changelog_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="history", size=32, color="#800000"),
                rx.heading("Histórico de Versões", size="6", color="#fafafa"),
                align="center",
                spacing="3",
                margin_bottom="1em"
            ),
            
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Versão", width="100px"),
                        rx.table.column_header_cell("Data", width="120px"),
                        rx.table.column_header_cell("Descrição"),
                    ),
                ),
                rx.table.body(
                    changelog_row("v2.0.3", "Jun/2026", "Feature Update: Criação de página dedicada para o Histórico de Versões, refatoração de navegação na sidebar."),
                    changelog_row("v2.0.2", "Jun/2026", "Patch Update: Correções de port binding para deploy no Render e ajustes na geração do relatório em PDF consolidado e individual."),
                    changelog_row("v2.0.1", "Jun/2026", "Patch Update: Correções na auto-migração Supabase, encriptação financeira e melhorias de UI no selector de hotéis."),
                    changelog_row("v2.0.0", "Jun/2026", "Major Release: Refatoração completa — migração de Streamlit para Reflex 0.9.4. Arquitetura full-stack reativa com frontend React, backend ASGI (Granian), estado gerenciado e UI 100% Python."),
                    changelog_row("v1.4.1", "Jun/2026", "Patch Update: Correção no cálculo de feriados móveis (Corpus Christi e Carnaval) e ajustes no linter."),
                    changelog_row("v1.4.0", "Mai/2026", "Minor Update: Painel de indicadores (KPI Cards) no topo do histórico com totalização de horas, ganhos estimados, chamados e média de tempo por atendimento."),
                    changelog_row("v1.3.1", "Mai/2026", "Patch de interface: filtros do Histórico unificados em linha única e correção de glitch visual no cabeçalho da tabela."),
                    changelog_row("v1.3.0", "Abr/2026", "Conformidade legal (LGPD) com aceite obrigatório de Termos de Uso."),
                    changelog_row("v1.2.3", "Abr/2026", "Novo motor de cálculo de duração e automação de fuso horário (Brasília)."),
                    changelog_row("v1.2.2", "Abr/2026", "Otimização de latência (migração para Ohio), upgrade de dados (chaves primárias para bigint/int8)."),
                    changelog_row("v1.2.1", "Abr/2026", "Hotfix crítico: reforço do Security Lock com normalização de perfil e bloqueio de fallback geral na query."),
                    changelog_row("v1.2.0", "Abr/2026", "Trava de segurança em relatórios (Security Lock), relatório \"Consolidado\" para Gestor/Admin, refatoração do cache."),
                    changelog_row("v1.1.0", "Abr/2026", "Pool de conexões PostgreSQL, snapshot salarial por registro, exclusão em massa, backup CSV automático."),
                    changelog_row("v1.0.0", "2026", "Versão inicial — autenticação, CRUD de registros, geração de PDF, gestão de hotéis e usuários."),
                ),
                width="100%",
                variant="surface",
                size="2",
            ),
            
            rx.button(
                "← Voltar ao Início",
                on_click=rx.redirect("/"),
                margin_top="2em",
                color_scheme="gray",
                variant="outline",
                cursor="pointer",
            ),
            
            width="100%",
            max_width="900px",
            align_items="center",
        ),
        width="100%",
        min_height="100vh",
        background_color="#0e1117",
        padding="2em",
    )
