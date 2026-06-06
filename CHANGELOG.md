# Changelog — Controle de Horas Extras

Todas as alterações relevantes deste projeto estão documentadas aqui.  
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.0.0] — 2026-06-06

> **Release Major — Refatoração Completa: Streamlit ➔ Reflex**

Esta versão representa a maior mudança arquitetural desde o lançamento do projeto.
O sistema foi reescrito do zero sobre o framework **Reflex 0.9.4**, eliminando as
limitações estruturais do Streamlit e entregando uma aplicação full-stack reativa,
com frontend compilado em React e backend FastAPI/ASGI.

### ✨ Novo

- **Framework Reflex 0.9.4** como base full-stack, substituindo integralmente o Streamlit
- **Gerenciamento de estado reativo** via classes `rx.State` com variáveis computadas (`@rx.var`), eliminando o modelo top-down de re-render do Streamlit
- **Sessão persistente nativa** com `rx.Cookie` criptografado (Fernet/AES), sem dependência de `extra-streamlit-components`
- **Arquitetura modular** em múltiplos `State`: `AuthState`, `DataState`, `FormState`, `HotelState`, `UsuarioState`
- **Servidor ASGI com Granian** para melhor performance e menor consumo de memória no Render
- **TailwindCSS v4** integrado via plugin nativo do Reflex (`TailwindV4Plugin`)
- **Sitemap automático** via `SitemapPlugin` do Reflex
- **UI 100% Python** — sem uso de `unsafe_allow_html`, injeção de CSS ou HTML manual
- **KPI Cards** e filtros de histórico construídos com componentes nativos do Reflex
- **Tabela de registros** com `rx.table.root` e suporte a checkboxes para exclusão em massa
- **Geração de PDF assíncrona** com ReportLab encapsulada para evitar bloqueio da UI
- **Backup CSV automático** com rotação dos 10 arquivos mais recentes por tabela
- **Compliance LGPD** — aceite de termos com gravação de timestamp em `America/Sao_Paulo`

### 🔄 Alterado

- `database.py` reescrito: pool de conexões SQLite com `contextmanager`, migrações idempotentes e log de segurança por perfil
- `report_generator.py` desacoplado da UI — gera PDF via chamada de backend sem travar a interface
- `models.py` migrado para `SQLModel` com tipos nativos (`Field`, `Optional`)
- `time_utils.py` refatorado para rodar de forma síncrona dentro do ciclo de vida do Reflex
- Hierarquia de perfis (`ADMIN`, `GESTOR`, `USER`) com **Security Lock** aplicado diretamente nas queries SQL
- Estrutura de diretórios reorganizada — pacote principal em `HorasExtras_Reflex/`
- Configuração centralizada em `rxconfig.py`

### 🗑️ Removido

- Dependência do **Streamlit** e todos os seus componentes (`st.session_state`, `st.rerun()`, `@st.fragment`, `st.fragment`)
- Dependência de `extra-streamlit-components` (cookie manager de terceiro)
- Dependência de **Pandas** — lógica de agrupamento migrada para Python puro
- Injeção de HTML/CSS via `unsafe_allow_html=True`
- Arquivos legados do Streamlit (preservados externamente em `Streamlit_legacy.zip`)

### 🔒 Segurança

- Senhas hasheadas com **Bcrypt** (salt individual por usuário)
- Salários criptografados em repouso com **Fernet (AES-128-CBC)**
- Security Lock por perfil: usuários `USER` nunca acessam dados de outros usuários, independente do filtro externo
- Log de segurança em cada consulta de chamados: `[SECURITY LOG] Perfil / LoggedUser / FilterRequested`
- `.env` excluído do repositório via `.gitignore`

### 📦 Dependências

| Pacote | Versão |
| --- | --- |
| reflex | 0.9.4 |
| bcrypt | 5.0.0 |
| cryptography | 48.0.0 |
| python-dotenv | 1.2.2 |
| reportlab | 4.5.1 |
| holidays | 0.98 |
| python-dateutil | 2.9.0.post0 |
| sqlmodel | 0.0.38 |
| granian | 2.7.5 |
| psycopg2-binary | 2.9.12 |
| pillow | 12.2.0 |

---

## [1.4.1] — 2025 (Streamlit — legado)

Última versão estável do sistema baseado em Streamlit.

- Framework: Streamlit 1.56.0
- Backend: Python 3.12 + SQLite / Supabase (PostgreSQL 15)
- Geração de PDF: ReportLab 4.4.10
- Deploy: Render (Streamlit Community Cloud com limitações de recursos)

> A partir da v2.0.0 esta versão é considerada descontinuada.
> O código-fonte está arquivado em `Streamlit_legacy.zip`.
