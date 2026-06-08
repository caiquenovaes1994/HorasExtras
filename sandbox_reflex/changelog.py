import reflex as rx

CHANGELOG_DATA = [
    {"versao": "v2.0.3", "data": "Jun/2026", "tipo": "Feature Update:", "detalhes": " Criação de página dedicada para o Histórico de Versões, refatoração de navegação na sidebar."},
    {"versao": "v2.0.2", "data": "Jun/2026", "tipo": "Patch Update:", "detalhes": " Correções de port binding para deploy no Render e ajustes na geração do relatório em PDF consolidado e individual."},
    {"versao": "v2.0.1", "data": "Jun/2026", "tipo": "Patch Update:", "detalhes": " Correções na auto-migração Supabase, encriptação financeira e melhorias de UI no selector de hotéis."},
    {"versao": "v2.0.0", "data": "Jun/2026", "tipo": "Major Release:", "detalhes": " Refatoração completa — migração de Streamlit para Reflex 0.9.4. Arquitetura full-stack reativa com frontend React, backend ASGI (Granian), estado gerenciado e UI 100% Python."},
    {"versao": "v1.4.1", "data": "Jun/2026", "tipo": "Patch Update:", "detalhes": " Correção no cálculo de feriados móveis (Corpus Christi e Carnaval) e ajustes no linter."},
    {"versao": "v1.4.0", "data": "Mai/2026", "tipo": "Minor Update:", "detalhes": " Painel de indicadores (KPI Cards) no topo do histórico com totalização de horas, ganhos estimados, chamados e média de tempo por atendimento."},
    {"versao": "v1.3.1", "data": "Mai/2026", "tipo": "Patch de interface:", "detalhes": " filtros do Histórico unificados em linha única e correção de glitch visual no cabeçalho da tabela."},
    {"versao": "v1.3.0", "data": "Abr/2026", "tipo": "Conformidade legal (LGPD):", "detalhes": " com aceite obrigatório de Termos de Uso."},
    {"versao": "v1.2.3", "data": "Abr/2026", "tipo": "Novo motor:", "detalhes": " de cálculo de duração e automação de fuso horário (Brasília)."},
    {"versao": "v1.2.2", "data": "Abr/2026", "tipo": "Otimização de latência:", "detalhes": " (migração para Ohio), upgrade de dados (chaves primárias para bigint/int8)."},
    {"versao": "v1.2.1", "data": "Abr/2026", "tipo": "Hotfix crítico:", "detalhes": " reforço do Security Lock com normalização de perfil e bloqueio de fallback geral na query."},
    {"versao": "v1.2.0", "data": "Abr/2026", "tipo": "Trava de segurança:", "detalhes": " em relatórios (Security Lock), relatório \"Consolidado\" para Gestor/Admin, refatoração do cache."},
    {"versao": "v1.1.0", "data": "Abr/2026", "tipo": "Features:", "detalhes": " Pool de conexões PostgreSQL, snapshot salarial por registro, exclusão em massa, backup CSV automático."},
    {"versao": "v1.0.0", "data": "2026", "tipo": "Versão inicial:", "detalhes": " autenticação, CRUD de registros, geração de PDF, gestão de hotéis e usuários."},
]

class ChangelogState(rx.State):
    page: int = 1
    items_per_page: int = 10
    
    @rx.var
    def total_pages(self) -> int:
        return (len(CHANGELOG_DATA) + self.items_per_page - 1) // self.items_per_page
        
    @rx.var
    def current_page_items(self) -> list[dict[str, str]]:
        start = (self.page - 1) * self.items_per_page
        return CHANGELOG_DATA[start:start + self.items_per_page]
        
    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            
    def prev_page(self):
        if self.page > 1:
            self.page -= 1

def changelog_row(item: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text(item["versao"], weight="bold", color="#2ecc71")),
        rx.table.cell(item["data"]),
        rx.table.cell(
            rx.text(
                rx.text(item["tipo"], color="#800000", weight="bold"),
                item["detalhes"],
            )
        ),
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
                    rx.foreach(
                        ChangelogState.current_page_items,
                        changelog_row
                    )
                ),
                width="100%",
                variant="surface",
                size="2",
            ),
            
            rx.hstack(
                rx.button(
                    "Anterior", 
                    on_click=ChangelogState.prev_page, 
                    disabled=ChangelogState.page == 1,
                    variant="soft",
                    color_scheme="gray",
                    cursor=rx.cond(ChangelogState.page == 1, "not-allowed", "pointer")
                ),
                rx.text(f"Página {ChangelogState.page} de {ChangelogState.total_pages}", size="2", color="#b0b0b8"),
                rx.button(
                    "Próxima", 
                    on_click=ChangelogState.next_page, 
                    disabled=ChangelogState.page == ChangelogState.total_pages,
                    variant="soft",
                    color_scheme="gray",
                    cursor=rx.cond(ChangelogState.page == ChangelogState.total_pages, "not-allowed", "pointer")
                ),
                width="100%",
                justify="between",
                align="center",
                margin_top="1em"
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
