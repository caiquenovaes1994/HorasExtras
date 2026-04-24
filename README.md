# ⏱️ Controle de Horas Extras

**Sistema profissional para gestão de atendimentos e controle de horas extras com geração de relatórios PDF de alta fidelidade.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://supabase.com/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF-lightgrey?style=for-the-badge)](https://www.reportlab.com/)
[![Version](https://img.shields.io/badge/version-1.2.1-2ecc71?style=for-the-badge)](RELEASE_NOTES_v1.2.1.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Hierarquia de Acesso](#hierarquia-de-acesso)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Execução](#instalação-e-execução)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Uso](#uso)
- [Histórico de Versões](#histórico-de-versões)
- [Autor](#autor)

---

## Sobre o Projeto

O **Controle de Horas Extras** é uma aplicação web desenvolvida com **Python e Streamlit** para automatizar o processo de registro, acompanhamento e validação de atendimentos realizados fora do expediente padrão.

O sistema gerencia todo o fluxo: desde o registro do chamado até a geração do relatório PDF (modelo **"Folha de Hora Extra"**) com cálculo automático de horas em **50%** ou **100%**, respeitando as regras de dias úteis, sábados, domingos e feriados nacionais brasileiros.

O banco de dados é hospedado em nuvem no **Supabase (PostgreSQL)**, garantindo alta disponibilidade, backups automáticos e compatibilidade com deploys em plataformas como o **Render**.

---

## Funcionalidades

### 🔐 Autenticação e Segurança

- **Sessão persistente** via Cookies Criptografados com auto-login seguro (token Fernet com validade de 24 horas).
- **Senhas protegidas** com hash Bcrypt (custo adaptativo).
- **Criptografia de dados sensíveis** (salários base) via AES/Fernet, em conformidade com a LGPD.
- **Troca de Senha Obrigatória** disparada automaticamente no primeiro acesso de novos usuários.
- **Security Lock em relatórios:** Usuários com perfil `USER` são restritos em nível de banco de dados — mesmo que tentem burlar a interface, a query sempre filtra pelo próprio `username`.

### 📋 Registro de Atendimentos

- Máscara de horário automática (ex: digitando `0730` → converte para `07:30`).
- Campo **Caso/INC opcional** para referência de incidentes.
- Seleção dinâmica de Hotel/PMS populada do banco de dados com **cache de 24 horas** para reduzir latência.
- Formulário isolado com **`@st.fragment`**, garantindo que interações não recarregam a página inteira.

### 📊 Relatório PDF de Alta Fidelidade

- **Calendário completo**: exibe todos os dias do período de competência (26 do mês anterior ao 25 do mês atual), mesmo os sem registro.
- Destaque automático com **fundo cinza (#D3D3D3)** em Sábados, Domingos e Feriados Nacionais.
- Cálculo automático de faturamento iterado linha a linha, baseado nos divisores legais para horas de **50%** (dias úteis e sábados) e **100%** (domingos e feriados).
- **Tabela Financeira Estruturada** com totais de Extra 50%, Extra 100% e Total Geral a Receber.
- **Relatório Consolidado**: gera um PDF multi-página com um colaborador por página, exclusivo para Gestores e Administradores.
- Layout otimizado para caber em **uma única página A4 paisagem** por colaborador.
- Cabeçalho profissional com **cor vinho corporativa** (#800000).

### 🏨 Gestão de Hotéis / PMS

- Cadastro e edição de hotéis via janela modal (`st.dialog`) com **fluxo de aprovação pelo Administrador**.
- Solicitações de criação, edição e exclusão são enfileiradas e aprovadas/rejeitadas pelo ADMIN.
- Integridade garantida com `ON CONFLICT` nativo do PostgreSQL.

### 👥 Gestão de Usuários (Admin)

- **CRUD completo** de usuários em interface modal dedicada.
- Definição de **perfil** (ADMIN, GESTOR, USER) e **salário base** na criação.
- Reset de senha administrativo com ativação automática de troca obrigatória.

### 💰 Trava de Base Financeira (Snapshot Salarial)

- **Snapshot no momento do registro:** O salário vigente é capturado de forma cifrada e atrelado individualmente a cada chamado.
- **Imutabilidade histórica:** Reajustes salariais futuros não afetam a integridade dos cálculos de meses anteriores.
- **Fallback inteligente:** Registros legados sem snapshot utilizam automaticamente o salário atual do perfil.

### 🗑️ Exclusão em Massa

- Seleção múltipla de registros no histórico via checkboxes.
- Confirmação de exclusão em massa via diálogo modal dedicado, com proteção contra ações acidentais.

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
| [Streamlit](https://streamlit.io) | 1.x | Interface web |
| [PostgreSQL / Supabase](https://supabase.com) | — | Banco de dados em nuvem |
| [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) | 2.9.11 | Driver PostgreSQL com pool de conexões |
| [ReportLab](https://reportlab.com) | 4.4 | Geração de relatórios PDF |
| [Pandas](https://pandas.pydata.org) | 3.x | Manipulação e agrupamento de dados |
| [holidays](https://pypi.org/project/holidays/) | 0.94 | Detecção de feriados nacionais (BR) |
| [bcrypt](https://pypi.org/project/bcrypt/) | — | Hash seguro de senhas |
| [cryptography](https://pypi.org/project/cryptography/) | — | Criptografia Fernet (AES) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | — | Carregamento de variáveis de ambiente |
| [extra-streamlit-components](https://pypi.org/project/extra-streamlit-components/) | 0.1.71 | Cookie Manager para sessão persistente |

---

## Estrutura do Projeto

```text
HorasExtras/
│
├── app.py                    # Interface principal (Streamlit) e controle de sessão
├── database.py               # Camada de acesso ao banco de dados (CRUD + criptografia + security lock)
├── report_generator.py       # Geração de relatórios em PDF (ReportLab)
├── utils.py                  # Funções auxiliares (cálculos, máscaras, período de competência)
├── migrate_sqlite_to_pg.py   # Script utilitário de migração SQLite → PostgreSQL
│
├── data/                     # Diretório de dados locais (ignorado pelo Git)
│   └── exports/              # Exportações CSV automáticas de backup
│
├── .env                      # Variáveis de ambiente (não versionado)
├── .env.example              # Modelo de referência para o .env
├── requirements.txt          # Dependências do projeto
├── start.bat                 # Script de inicialização automática (Windows)
├── RELEASE_NOTES_v1.2.md     # Notas da versão 1.2.0
├── RELEASE_NOTES_v1.2.1.md   # Notas da versão atual (hotfix)
└── README.md
```

---

## Instalação e Execução

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado e disponível no `PATH`
- Uma instância do **Supabase** criada (plano gratuito é suficiente)

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/caiquenovaes1994/HorasExtras.git
cd HorasExtras
```

#### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (ou copie o `.env.example`) e preencha com suas credenciais:

```env
SECRET_KEY=sua_chave_fernet_aqui
ADMIN_PWD=sua_senha_admin_inicial

# Conexão PostgreSQL (Supabase)
DB_HOST=aws-0-sa-east-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.seu_project_id
DB_PASS=sua_senha_do_supabase
```

> **⚠️ Importante:** A `SECRET_KEY` deve ser um token Fernet válido. Gere um com:
>
> ```bash
> python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
> ```

**ℹ️ Credenciais Supabase:** Acesse **Project Settings → Database → Connection pooling** e use o host/porta do **Transaction Pooler** (porta `6543`) para compatibilidade com IPv4.

#### 3. Execute o script de inicialização

O arquivo `start.bat` automatiza todo o processo: cria o ambiente virtual, instala as dependências e inicia o servidor na porta `3003`.

```powershell
./start.bat
```

#### 4. (Opcional) Migrar dados de SQLite anterior

```bash
python migrate_sqlite_to_pg.py
```

As tabelas são criadas automaticamente na primeira execução do app. Este passo é necessário apenas para migrar dados de uma instância SQLite legada.

#### 5. Acesse a aplicação no navegador

```text
http://localhost:3003
```

> **Login padrão (primeiro acesso):** Use as credenciais definidas no `.env`. O sistema exigirá a troca de senha obrigatoriamente.

---

## Variáveis de Ambiente

| Variável | Descrição | Obrigatória |
| :--- | :--- | :---: |
| `SECRET_KEY` | Chave Fernet para criptografia de dados sensíveis e tokens de sessão | ✅ |
| `ADMIN_PWD` | Senha inicial do usuário administrador padrão (`cnovaes`) | ✅ |
| `DB_HOST` | Host do banco PostgreSQL (Transaction Pooler do Supabase) | ✅ |
| `DB_PORT` | Porta de conexão (use `6543` para o Transaction Pooler) | ✅ |
| `DB_NAME` | Nome do banco de dados (padrão: `postgres`) | ✅ |
| `DB_USER` | Usuário do banco (formato: `postgres.seu_project_id`) | ✅ |
| `DB_PASS` | Senha do banco de dados | ✅ |

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
| **v1.2.1** | Abr/2026 | Hotfix crítico: reforço do Security Lock com normalização de perfil e bloqueio de fallback geral na query. |
| **v1.2.0** | Abr/2026 | Trava de segurança em relatórios (Security Lock), relatório "Consolidado" para Gestor/Admin, refatoração do cache. |
| **v1.1.0** | Abr/2026 | Pool de conexões PostgreSQL, snapshot salarial por registro, exclusão em massa, backup CSV automático. |
| **v1.0.0** | 2026 | Versão inicial — autenticação, CRUD de registros, geração de PDF, gestão de hotéis e usuários. |

> Veja as notas completas da versão atual em [RELEASE_NOTES_v1.2.1.md](RELEASE_NOTES_v1.2.1.md).

---

## Autor

Desenvolvido por **Caique Novaes**

- E-mail: [caiquenovaes1994@gmail.com](mailto:caiquenovaes1994@gmail.com)
- GitHub: [@caiquenovaes1994](https://github.com/caiquenovaes1994)

---

Desenvolvido com ☕ e Python · 2026 · v1.2.1
