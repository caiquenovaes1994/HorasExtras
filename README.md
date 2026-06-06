# ⏱️ Controle de Horas Extras — v2.0.0

> Sistema interno de controle de horas extras para equipes de suporte hoteleiro.  
> Reescrito do zero com **[Reflex](https://reflex.dev/) 0.9.4** — full-stack Python, frontend reativo compilado em React.

---

## 📋 Funcionalidades

| Módulo | Descrição |
|---|---|
| 🔐 **Autenticação** | Login com sessão persistente via cookie Fernet/AES + Bcrypt |
| 📝 **Novo Registro** | Cadastro de chamados com validação de horário e cruzamento de meia-noite |
| 📊 **Histórico** | Filtros por plantonista, mês e ano + KPI Cards (horas, ganhos, chamados, média) |
| 🏨 **Gestão de Hotéis** | CRUD com fluxo de aprovação (solicitação → ADMIN aprova/rejeita) |
| 👥 **Gestão de Usuários** | CRUD completo com hierarquia de perfis: `ADMIN`, `GESTOR`, `USER` |
| 📄 **Relatório PDF** | Geração de folha de hora extra individual ou em massa via ReportLab |
| 🔒 **Compliance LGPD** | Aceite de termos obrigatório com registro de timestamp |

---

## 🏗️ Arquitetura

```
HorasExtras/
├── HorasExtras_Reflex/          # Pacote principal
│   ├── sandbox_reflex.py        # App Reflex — páginas e rotas
│   ├── state.py                 # AuthState — autenticação e sessão
│   ├── data_state.py            # DataState — histórico e KPIs
│   ├── state_form.py            # FormState — CRUD de chamados
│   ├── state_hoteis.py          # HotelState — gestão de hotéis
│   ├── state_usuarios.py        # UsuarioState — gestão de usuários
│   ├── database.py              # Camada de dados (SQLite + Fernet + Bcrypt)
│   ├── models.py                # Modelos SQLModel
│   ├── report_generator.py      # Gerador de PDF (ReportLab)
│   ├── time_utils.py            # Cálculos de tempo, feriados, períodos
│   └── backup_utils.py          # Backup automático CSV com rotação
├── assets/                      # Favicon e assets estáticos
├── rxconfig.py                  # Configuração Reflex
├── requirements.txt             # Dependências pinadas
├── .env                         # Credenciais (não versionado)
└── CHANGELOG.md                 # Histórico de versões
```

---

## 🚀 Rodando localmente

### Pré-requisitos

- Python 3.12+
- [Bun](https://bun.sh/) (para o build do frontend Reflex)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/caiquenovaes1994/HorasExtras.git
cd HorasExtras

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env         # edite com suas credenciais
```

### Variáveis de ambiente (`.env`)

```env
SECRET_KEY=<chave-fernet-base64>   # gerada com Fernet.generate_key()
ADMIN_PWD=<senha-admin-inicial>
DB_HOST=<host-supabase>
DB_NAME=<nome-do-banco>
DB_USER=<usuario>
DB_PASS=<senha>
DB_PORT=5432
```

### Executar

```bash
reflex run
```

A aplicação estará disponível em `http://localhost:3000`.

---

## ☁️ Deploy (Render)

O projeto está configurado para deploy no [Render](https://render.com/).

| Configuração | Valor |
|---|---|
| **Runtime** | Python 3.12 |
| **Build Command** | `pip install -r requirements.txt && reflex export --no-zip` |
| **Start Command** | `reflex run --env prod` |

As variáveis do `.env` devem ser configuradas como **Environment Variables** no painel do Render.

---

## 🔒 Segurança

- **Senhas** hasheadas com Bcrypt (salt individual)
- **Salários** criptografados em repouso com Fernet (AES-128-CBC)
- **Security Lock por perfil:** usuários `USER` só acessam seus próprios registros — a trava é aplicada diretamente na query SQL, independente de parâmetros externos
- **Logs de auditoria:** cada consulta de chamados registra `Perfil / LoggedUser / FilterRequested` no console

---

## 📦 Stack

| Camada | Tecnologia |
|---|---|
| Framework | Reflex 0.9.4 |
| Frontend | React (compilado pelo Reflex) + TailwindCSS v4 |
| Servidor | Granian (ASGI) |
| Banco de dados | SQLite (local) / PostgreSQL — Supabase (produção) |
| ORM | SQLModel 0.0.38 |
| Criptografia | Bcrypt 5.0 + Cryptography 48 (Fernet) |
| PDF | ReportLab 4.5.1 |
| Feriados | holidays 0.98 + python-dateutil |

---

## 📄 Changelog

Consulte o [CHANGELOG.md](./CHANGELOG.md) para o histórico completo de versões.

---

## 🗂️ Histórico de decisões

- [ISSUE_refactor_framework.md](./ISSUE_refactor_framework.md) — Motivação e critérios para migração do Streamlit para Reflex
- [ROADMAP_REFLEX.md](./ROADMAP_REFLEX.md) — Plano de migração original (concluído na v2.0.0)

---

> **v1.4.1 (Streamlit)** — versão anterior arquivada em `Streamlit_legacy.zip` · descontinuada
