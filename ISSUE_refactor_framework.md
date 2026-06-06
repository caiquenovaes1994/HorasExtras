# [Refactor] Migração do Streamlit para framework mais leve (Reflex ou Flet)

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

- [ ] Autenticação com sessão persistente (cookie com token Fernet)
- [ ] CRUD de chamados (Novo Registro, Edição, Exclusão, Visualização)
- [ ] Histórico com filtros e KPI Cards
- [ ] Gestão de Hotéis com fluxo de aprovação
- [ ] Gestão de Usuários (ADMIN)
- [ ] Geração de PDF com ReportLab (pode ser via endpoint/backend)
- [ ] Hierarquia de perfis (ADMIN, GESTOR, USER) com Security Lock no banco
- [ ] Compliance LGPD (aceite de termos)

---

## 🔬 Próximos Passos

1. **Protótipo com Reflex:** Criar um protótipo da tela de Login + Histórico para avaliar a experiência de desenvolvimento.
2. **Protótipo com Flet:** Idem para Flet, especialmente avaliar a viabilidade do deploy web.
3. **Benchmark comparativo:** Avaliar tamanho do bundle, tempo de carregamento e consumo de memória.
4. **Decisão:** Documentar a decisão técnica e criar um plano de migração incremental por módulo.

---

## 🏷️ Contexto Atual

- **Versão atual:** v1.4.1
- **Framework atual:** Streamlit 1.56.0
- **Backend:** Python 3.12 + Supabase (PostgreSQL 15)
- **Geração de PDF:** ReportLab 4.4.10

---

> **Nota:** Esta issue é de natureza exploratória. A migração só será iniciada após a conclusão do estudo comparativo e validação dos protótipos.
