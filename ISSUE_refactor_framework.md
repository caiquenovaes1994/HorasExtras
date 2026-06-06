# ✅ [FECHADA — v2.0.0] Migração do Streamlit para framework mais leve (Reflex)

## 🎯 Objetivo

Refatorar a interface do sistema, substituindo o **Streamlit** por um framework Python mais leve, moderno e com melhor controle sobre a UI, tendo como principais candidatos:

- [**Reflex**](https://reflex.dev/) — Framework full-stack Python com componentes reativos e estado gerenciado, compila para React no frontend.
- [**Flet**](https://flet.dev/) — Framework baseado em Flutter para criar apps desktop, mobile e web com Python puro.

---

## 🔍 Motivação / Problema atual

O Streamlit apresenta limitações estruturais que se tornam cada vez mais evidentes conforme o projeto cresce:

- **Re-renders excessivos:** Qualquer interação (clique, seleção) re-executa o script inteiro de cima a baixo — workarounds como `@st.fragment` só aliviam parcialmente.
- **Gerenciamento de estado frágil:** `st.session_state` é funcional, mas propenso a bugs sutis (ex: widgets "instanciados" após reset, necessidade de `st.rerun()` manual).
- **Controle de UI limitado:** Customizações de layout e CSS requerem injeção de HTML/CSS via `unsafe_allow_html=True`, o que é um anti-padrão.
- **Cookie Manager externo:** Dependência de `extra-streamlit-components` para gerenciar cookies é frágil e não oficial.
- **Performance:** O modelo de execução top-down é ineficiente para aplicações com múltiplas abas e estados complexos.
- **Deploy:** Streamlit Community Cloud tem limitações de recursos para apps com banco de dados externo (Supabase/PostgreSQL).

---

## 📋 Escopo do Estudo

### Critérios de Avaliação

| Critério | Peso |
| --- | --- |
| Controle de estado (reatividade) | Alto |
| Facilidade de manutenção | Alto |
| Suporte a autenticação/cookies nativos | Médio |
| Performance percebida pelo usuário | Alto |
| Curva de aprendizado | Médio |
| Deploy (compatibilidade com Supabase/PostgreSQL) | Alto |

### Funcionalidades que devem ser preservadas

- [x] Autenticação com sessão persistente (cookie com token Fernet)
- [x] CRUD de chamados (Novo Registro, Edição, Exclusão, Visualização)
- [x] Histórico com filtros e KPI Cards
- [x] Gestão de Hotéis com fluxo de aprovação
- [x] Gestão de Usuários (ADMIN)
- [x] Geração de PDF com ReportLab (via backend desacoplado)
- [x] Hierarquia de perfis (ADMIN, GESTOR, USER) com Security Lock no banco
- [x] Compliance LGPD (aceite de termos)

---

## ✅ Resolução

**Framework escolhido: Reflex** — migração concluída na v2.0.0 (2026-06-06).

- Reflex foi selecionado pela sua arquitetura full-stack Python nativa, suporte a cookies nativos, estado reativo e deploy compatível com Render.
- Flet foi descartado por limitações no deploy web e maturidade do ecossistema.
- A migração completa foi realizada de forma isolada (sandbox), sem impacto na v1.4.1 em produção durante o desenvolvimento.

---

## 🏷️ Contexto

| | v1.4.1 (legado) | v2.0.0 (atual) |
|---|---|---|
| **Framework** | Streamlit 1.56.0 | Reflex 0.9.4 |
| **Frontend** | Streamlit nativo | React (compilado pelo Reflex) + TailwindCSS v4 |
| **Servidor** | Uvicorn | Granian (ASGI) |
| **Backend** | Python 3.12 | Python 3.12 |
| **Banco** | SQLite / Supabase (PostgreSQL 15) | SQLite / Supabase (PostgreSQL 15) |
| **PDF** | ReportLab 4.4.10 | ReportLab 4.5.1 |
| **Status** | ⛔ Descontinuado | ✅ Em produção |

---

> **Nota:** Issue encerrada. Código legado arquivado em `Streamlit_legacy.zip`. Consulte o [CHANGELOG.md](./CHANGELOG.md) para o detalhamento completo da v2.0.0.
