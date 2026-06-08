# ⏱️ Controle de Horas Extras

**Sistema profissional para gestão de atendimentos e controle de horas extras com geração de relatórios PDF de alta fidelidade.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Reflex](https://img.shields.io/badge/Reflex-0.9.4-6C47FF?style=flat&logo=reflex&logoColor=white)](https://reflex.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)](https://supabase.com/)
[![ReportLab](https://img.shields.io/badge/ReportLab-4.5.1-lightgrey?style=flat)](https://www.reportlab.com/)
[![Version](https://img.shields.io/badge/version-2.0.2-2ecc71?style=flat)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Hierarquia de Acesso](#hierarquia-de-acesso)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Uso](#uso)
- [Histórico de Versões](#histórico-de-versões)
- [Autor](#autor)

---

## Sobre o Projeto

O **Controle de Horas Extras** é uma aplicação web full-stack desenvolvida com **Python e [Reflex](https://reflex.dev/)** para automatizar o processo de registro, acompanhamento e validação de atendimentos realizados fora do expediente padrão.

O sistema gerencia todo o fluxo: desde o registro do chamado até a geração do relatório PDF (modelo **"Folha de Hora Extra"**) com cálculo automático de horas em **50%** ou **100%**, respeitando as regras de dias úteis, sábados, domingos e feriados nacionais brasileiros.

O banco de dados é hospedado em nuvem no **Supabase (PostgreSQL)** localizado na região **Ohio (us-east-2)**, garantindo alta disponibilidade, backups automáticos e altíssima performance.

---

## Funcionalidades

### 🔐 Autenticação e Segurança

- **Sessão persistente** via `rx.Cookie` criptografado com token Fernet (validade de 24 horas).
- **Senhas protegidas** com hash Bcrypt (custo adaptativo).
- **Criptografia de dados sensíveis** (salários base) via AES/Fernet, em conformidade com a LGPD.
- **Troca de Senha Obrigatória** disparada automaticamente no primeiro acesso de novos usuários.
- **Security Lock em relatórios:** Usuários com perfil `USER` são restritos em nível de banco de dados — mesmo que tentem burlar a interface, a query sempre filtra pelo próprio `username`.

### 📋 Registro de Atendimentos

- Máscara de horário automática (ex: digitando `0730` → converte para `07:30`).
- Campo **Caso/INC opcional** para referência de incidentes.
- Seleção dinâmica de Hotel/PMS populada do banco de dados.
- Formulário reativo com **estado gerenciado** (`FormState`), sem re-render de página inteira.

### 📊 Relatório PDF de Alta Fidelidade

- **Calendário completo**: exibe todos os dias do período de competência (26 do mês anterior ao 25 do mês atual), mesmo os sem registro.
- Destaque automático com **fundo cinza (#D3D3D3)** em Sábados, Domingos e Feriados Nacionais.
- Cálculo automático de faturamento iterado linha a linha, baseado nos divisores legais para horas de **50%** (dias úteis e sábados) e **100%** (domingos e feriados).
- **Tabela Financeira Estruturada** com totais de Extra 50%, Extra 100% e Total Geral a Receber.
- **Relatório Consolidado**: gera um PDF multi-página com um colaborador por página, exclusivo para Gestores e Administradores.
- Layout otimizado para caber em **uma única página A4 paisagem** por colaborador.
- Cabeçalho profissional com **cor vinho corporativa** (#800000).
- **Geração assíncrona**: a criação do PDF roda em background, sem travar a interface do usuário.

### 🏨 Gestão de Hotéis / PMS

- Cadastro e edição de hotéis com **fluxo de aprovação pelo Administrador**.
- Solicitações de criação, edição e exclusão são enfileiradas e aprovadas/rejeitadas pelo ADMIN.
- Integridade garantida com `ON CONFLICT` nativo do banco de dados.

### 👥 Gestão de Usuários (Admin)

- **CRUD completo** de usuários em interface dedicada.
- Definição de **perfil** (ADMIN, GESTOR, USER) e **salário base** na criação.
- Reset de senha administrativo com ativação automática de troca obrigatória.

### 💰 Trava de Base Financeira (Snapshot Salarial)

- **Snapshot no momento do registro:** O salário vigente é capturado de forma cifrada e atrelado individualmente a cada chamado.
- **Imutabilidade histórica:** Reajustes salariais futuros não afetam a integridade dos cálculos de meses anteriores.
- **Fallback inteligente:** Registros legados sem snapshot utilizam automaticamente o salário atual do perfil.

### 📊 Dashboard de Indicadores (KPI Cards)

- **Acompanhamento em Tempo Real:** 4 cartões de indicadores (KPIs) exibidos no topo do histórico de atendimentos.
- **Métricas Consolidadas:** Totais de horas 50% e 100%, ganhos brutos estimados, contagem de chamados e duração média.
- **Reatividade nativa:** KPIs recalculam automaticamente ao alterar filtros de competência, sem re-render manual.

### 🗑️ Exclusão em Massa

- Seleção múltipla de registros no histórico via checkboxes.
- Confirmação de exclusão em massa com proteção contra ações acidentais.

### 💾 Backup Local (CSV)

- A cada operação de escrita, as tabelas `chamados` e `usuarios` são exportadas para arquivos CSV locais.
- **Rotação automática** mantendo os 10 exports mais recentes por tabela.
- Complementa os backups automáticos diários do Supabase.

---

## Hierarquia de Acesso

O sistema opera com três níveis de permissão, garantindo segregação funcional e segurança de dados:

| Perfil | Leitura | Escrita | Gestão de Usuários | Relatório Consolidado | Aprovações |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ADMIN** | Total | Total | ✅ | ✅ | ✅ |
| **GESTOR** | Total | ❌ | ❌ | ✅ | ❌ |
| **USER** | Próprios registros | Próprios registros | ❌ | ❌ | ❌ |

- **ADMIN:** Controle total do sistema — CRUD de registros, hotéis, usuários, aprovação de solicitações e emissão de relatórios individuais e consolidados.
- **GESTOR:** Perfil de auditoria/leitura. Visualiza todos os registros de todos os colaboradores e gera relatórios individuais ou consolidados, sem poder criar, editar ou excluir dados.
- **USER:** Acesso restrito aos próprios registros. A **Trava de Segurança (v1.2.1)** garante que, mesmo em caso de tentativa de manipulação da interface, o banco de dados nunca retorna dados de outros colaboradores.

---

## Tecnologias

| Tecnologia | Versão | Finalidade |
| :--- | :--- | :--- |
| [Python](https://python.org) | 3.12 | Linguagem principal |
| [Reflex](https://reflex.dev) | 0.9.4 | Framework full-stack (Python → React) |
| [Granian](https://github.com/emmett-framework/granian) | 2.7.5 | Servidor ASGI de alta performance |
| [PostgreSQL / Supabase](https://supabase.com) | 15 | Banco de dados em nuvem |
| [SQLModel](https://sqlmodel.tiangolo.com) | 0.0.38 | ORM (modelos e queries) |
| [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) | 2.9.12 | Driver PostgreSQL |
| [ReportLab](https://reportlab.com) | 4.5.1 | Geração de relatórios PDF |
| [holidays](https://pypi.org/project/holidays/) | 0.98 | Detecção de feriados nacionais (BR) |
| [bcrypt](https://pypi.org/project/bcrypt/) | 5.0.0 | Hash seguro de senhas |
| [cryptography](https://pypi.org/project/cryptography/) | 48.0.0 | Criptografia Fernet (AES) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.2.2 | Carregamento de variáveis de ambiente |
| [TailwindCSS v4](https://tailwindcss.com) | — | Estilização (via plugin nativo do Reflex) |

---

## Estrutura do Projeto

```text
HorasExtras/
│
├── sandbox_reflex/               # Pacote principal da aplicação
│   ├── __init__.py               # Inicializador do pacote
│   ├── sandbox_reflex.py         # App Reflex — páginas, rotas e componentes UI
│   ├── login.py                  # Componente de tela de login
│   ├── state.py                  # AuthState — autenticação, sessão e cookies
│   ├── data_state.py             # DataState — histórico, filtros e KPIs
│   ├── state_form.py             # FormState — CRUD de chamados
│   ├── state_hoteis.py           # HotelState — gestão de hotéis e aprovações
│   ├── state_usuarios.py         # UsuarioState — gestão de usuários (Admin)
│   ├── database.py               # Camada de acesso ao banco (CRUD + criptografia + security lock)
│   ├── models.py                 # Modelos SQLModel (Chamado, Hotel, Usuario, SolicitacaoHotel)
│   ├── report_generator.py       # Geração de relatórios em PDF (ReportLab)
│   ├── time_utils.py             # Cálculos de tempo, feriados e período de competência
│   └── backup_utils.py           # Backup automático CSV com rotação
│
├── assets/                       # Favicon e assets estáticos
│   ├── favicon.ico
│   └── relogio.png
│
├── rxconfig.py                   # Configuração do Reflex (app_name, plugins, db_url)
├── requirements.txt              # Dependências do projeto (pinadas)
├── .env                          # Variáveis de ambiente (não versionado)
├── CHANGELOG.md                  # Histórico completo de versões
├── ISSUE_refactor_framework.md   # Motivação e decisão técnica da migração
├── ROADMAP_REFLEX.md             # Plano de migração (concluído na v2.0.0)
├── LICENSE                       # Licença MIT
└── README.md
```

---

## Uso

O comportamento da interface varia conforme o **perfil do usuário logado**:

### Perfil USER

1. **Faça login** com suas credenciais. Na primeira vez, troque a senha obrigatória.
2. Na aba **"📝 Novo Registro"**, registre o atendimento informando data, hotel, horários e motivo.
3. Na aba **"📋 Histórico"**, visualize e edite seus próprios registros.
4. Na sidebar, selecione o **mês e ano** e clique em **"🚀 Gerar PDF"** para baixar sua Folha de Hora Extra pessoal.

### Perfil GESTOR

1. Todas as abas acima, mas **sem permissão de edição ou exclusão**.
2. No **"📋 Histórico"**, filtre por plantonista para visualizar os registros de qualquer colaborador.
3. Na sidebar, selecione **um colaborador específico** ou **"Consolidado"** para gerar o relatório de todos os colaboradores em um único PDF.

### Perfil ADMIN

1. Todas as funcionalidades do GESTOR.
2. Na aba **"⚙️ Usuários"**, crie, edite ou redefina senhas de usuários.
3. Na aba **"🏨 Hotéis"**, sugira e edite hotéis (as alterações ficam pendentes até aprovação).
4. Na aba **"🔔 Aprovações"**, aprove ou rejeite solicitações de criação/edição/exclusão de hotéis.

---

## Histórico de Versões

| Versão | Data | Descrição |
| :--- | :--- | :--- |
| **v2.0.2** | Jun/2026 | Patch Update: Correções de port binding para deploy no Render e ajustes na geração do relatório em PDF consolidado e individual. |
| **v2.0.1** | Jun/2026 | Patch Update: Correções na auto-migração Supabase, encriptação financeira e melhorias de UI no selector de hotéis. |
| **v2.0.0** | Jun/2026 | **Major Release:** Refatoração completa — migração de Streamlit para Reflex 0.9.4. Arquitetura full-stack reativa com frontend React, backend ASGI (Granian), estado gerenciado e UI 100% Python. |
| **v1.4.1** | Jun/2026 | Patch Update: Correção no cálculo de feriados móveis (Corpus Christi e Carnaval) e ajustes no linter. |
| **v1.4.0** | Mai/2026 | Minor Update: Painel de indicadores (KPI Cards) no topo do histórico com totalização de horas, ganhos estimados, chamados e média de tempo por atendimento. |
| **v1.3.1** | Mai/2026 | Patch de interface: filtros do Histórico unificados em linha única e correção de glitch visual no cabeçalho da tabela. |
| **v1.3.0** | Abr/2026 | Conformidade legal (LGPD) com aceite obrigatório de Termos de Uso. |
| **v1.2.3** | Abr/2026 | Novo motor de cálculo de duração e automação de fuso horário (Brasília). |
| **v1.2.2** | Abr/2026 | Otimização de latência (migração para Ohio), upgrade de dados (chaves primárias para bigint/int8). |
| **v1.2.1** | Abr/2026 | Hotfix crítico: reforço do Security Lock com normalização de perfil e bloqueio de fallback geral na query. |
| **v1.2.0** | Abr/2026 | Trava de segurança em relatórios (Security Lock), relatório "Consolidado" para Gestor/Admin, refatoração do cache. |
| **v1.1.0** | Abr/2026 | Pool de conexões PostgreSQL, snapshot salarial por registro, exclusão em massa, backup CSV automático. |
| **v1.0.0** | 2026 | Versão inicial — autenticação, CRUD de registros, geração de PDF, gestão de hotéis e usuários. |

---

## Autor

Desenvolvido por **Caique Novaes**

[![GitHub](https://img.shields.io/badge/GitHub-caiquenovaes1994-181717?style=flat&logo=github&logoColor=white)](https://github.com/caiquenovaes1994)
&nbsp;
[![Gmail](https://img.shields.io/badge/Gmail-caiquenovaes1994@gmail.com-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:caiquenovaes1994@gmail.com)

---

Desenvolvido com ☕ e Python · 2026 · v2.0.2
