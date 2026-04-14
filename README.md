# ⏱️ Controle de Horas Extras

**Sistema profissional para gestão de atendimentos e controle de horas extras com geração de relatórios PDF de alta fidelidade.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF-lightgrey?style=for-the-badge)](https://www.reportlab.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Hierarquia de Acesso](#hierarquia-de-acesso)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Execução](#instalação-e-execução)
- [Uso](#uso)
- [Autor](#autor)

---

## Sobre o Projeto

O **Controle de Horas Extras** é uma aplicação web desenvolvida com **Python e Streamlit** para automatizar o processo de registro, acompanhamento e validação de atendimentos realizados fora do expediente padrão.

O sistema gerencia todo o fluxo: desde o registro do chamado até a geração do relatório PDF (modelo "Folha de Hora Extra") com cálculo automático de horas em **50%** ou **100%**, obedecendo as regras de dias úteis, sábados, domingos e feriados nacionais.

---

## Funcionalidades

### Autenticação e Segurança

- Sessão persistente via **Cookies Criptografados** com auto-login seguro (token Fernet com validade de 24 horas).
- Senhas protegidas com **hash bcrypt** escalável.
- Proteção de dados sensíveis (salários base) por **Criptografia Simétrica (AES / Fernet)** para conformidade direta com a LGPD.
- **Troca de Senha Obrigatória** disparada automaticamente no primeiro acesso de novos usuários.

### Hierarquia de Acesso

O sistema opera com três níveis de permissão, garantindo segregação funcional:

| Perfil | Leitura | Escrita | Gestão de Usuários | Aprovações |
| :--- | :--- | :--- | :--- | :--- |
| **ADMIN** | Total | Total | Total | Total |
| **GESTOR** | Total | Nenhuma | Nenhuma | Nenhuma |
| **USER** | Próprios registros | Próprios registros | Nenhuma | Nenhuma |

- **ADMIN:** Controle total do sistema — CRUD de registros, hotéis, usuários e aprovação de solicitações.
- **GESTOR:** Perfil de auditoria/leitura. Visualiza todos os registros de todos os colaboradores, gera relatórios individuais e consolidados, mas não pode criar, editar ou excluir dados.
- **USER:** Acesso restrito aos próprios registros — cadastro de atendimentos, visualização e edição do histórico pessoal.

### Gestão de Hotéis / PMS

- Cadastro e edição de hotéis via **janela modal** (`st.dialog`) com fluxo de aprovação.
- Solicitações de criação, edição e exclusão passam por aprovação do Administrador.
- **Base Externa Opcional:** O sistema referencia um arquivo `data/hotels_source.sqlite` para carga massificada de clientes. Caso o arquivo não exista, o sistema opera de forma autônoma com hotéis inseridos manualmente.
- Garantia de registros únicos com `SELECT DISTINCT` (sem duplicações).

### Gestão de Usuários (Admin)

- **CRUD completo** de usuários em interface modal dedicada.
- Definição de perfil (ADMIN, GESTOR, USER) e salário base na criação.
- Reset de senha com flag de troca obrigatória.

### Trava de Base Financeira (Snapshot Salarial)

- **Captura via Snapshot:** O salário vigente é capturado de forma cifrada e atrelado individualmente a cada registro no momento da criação.
- **Imutabilidade Histórica:** Reajustes salariais (aumentos e dissídios) aplicados ao perfil do usuário não afetam a integridade dos cálculos financeiros de relatórios de meses anteriores.
- **Fallback Inteligente:** Registros legados sem snapshot utilizam automaticamente o salário atual do perfil como base de cálculo.

### Registro de Atendimentos

- Máscara de horário automática (ex: digitando `0730` → converte para `07:30`).
- Campo Caso/INC **opcional** para referência de incidentes.
- Seleção dinâmica de Hotel/PMS populada diretamente do banco de dados.
- Suporte a múltiplos turnos (Plantão 1, 2 e 3) por dia.

### Relatório PDF de Alta Fidelidade

- **Calendário completo**: exibe todos os dias do período de competência (26 do mês anterior ao 25 do mês atual), mesmo os sem registro.
- Destaque automático com **fundo cinza (#D3D3D3)** em Sábados, Domingos e Feriados.
- Cálculo automático de faturamento iterado (linha a linha) baseando-se nos divisores legais para horas de **50%** (dias úteis e sábados) e **100%** (domingos e feriados).
- **Tabela Financeira Estruturada** com totais de Extra 50%, Extra 100% e Total Geral a Receber.
- **Relatório Consolidado ("TODOS")**: Gera um PDF multi-página com um colaborador por página, ideal para gestores e administradores.
- Ajuste automático para caber em **uma única página A4 paisagem** por colaborador.
- Cabeçalho profissional com destaque em **cor vinho corporativa** (#800000).
- Tipografia Inter/Calibri com fallback automático para Helvetica.

### Exclusão em Massa

- Seleção múltipla de registros no histórico via checkboxes.
- Confirmação de exclusão em massa via diálogo modal dedicado.

---

## Tecnologias

| Tecnologia | Versão | Finalidade |
| :--- | :--- | :--- |
| [Python](https://python.org) | 3.12 | Linguagem principal |
| [Streamlit](https://streamlit.io) | 1.56 | Interface web |
| [SQLite](https://sqlite.org) | — | Banco de dados local |
| [ReportLab](https://reportlab.com) | 4.4 | Geração de relatórios PDF |
| [Pandas](https://pandas.pydata.org) | 3.0 | Manipulação e agrupamento de dados |
| [holidays](https://pypi.org/project/holidays/) | 0.94 | Detecção de feriados nacionais (BR) |
| [bcrypt](https://pypi.org/project/bcrypt/) | — | Hash seguro de senhas |
| [cryptography](https://pypi.org/project/cryptography/) | — | Criptografia Fernet (AES) |
| [extra-streamlit-components](https://pypi.org/project/extra-streamlit-components/) | 0.1.71 | Cookie Manager para sessão persistente |

---

## Estrutura do Projeto

```text
HorasExtras/
│
├── app.py               # Interface principal (Streamlit) e controle de sessão
├── database.py          # Camada de acesso ao banco de dados (CRUD + criptografia)
├── report_generator.py  # Geração de relatórios em PDF (ReportLab)
├── utils.py             # Funções auxiliares (cálculos, máscaras, período)
│
├── data/                # Diretório de dados locais (ignorado pelo Git)
│   ├── horas_extras.db  # Banco de dados principal (SQLite)
│   └── backups/         # Backups automáticos do banco de dados
│
├── .env                 # Variáveis de ambiente (SECRET_KEY, ADMIN_PWD)
├── .env.example         # Modelo de referência para o .env
├── requirements.txt     # Dependências do projeto
├── start.bat            # Script de inicialização automática (Windows)
└── README.md
```

---

## Instalação e Execução

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado e disponível no `PATH`

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/caiquenovaes1994/HorasExtras.git
cd HorasExtras
```

#### 2. Configuração de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (ou copie o `.env.example`) com as seguintes chaves:

```env
SECRET_KEY=sua_chave_fernet_aqui
ADMIN_PWD=sua_senha_admin_inicial
```

> **Nota:** A `SECRET_KEY` deve ser um token Fernet válido de 32 bytes codificado em Base64. Gere uma com: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.

#### 3. Execute o script de inicialização

O arquivo `start.bat` automatiza todo o processo: cria o ambiente virtual, instala as dependências e inicia o servidor.

```powershell
./start.bat
```

#### 4. Acesse a aplicação no navegador

```text
http://localhost:3003
```

> **Login padrão (primeiro acesso):** Utilize as credenciais de administrador definidas no arquivo `.env`. O sistema exigirá a troca de senha no primeiro login.

---

## Uso

1. **Faça login** com as suas credenciais.
2. Na aba **"📝 Novo Registro"**, registre o atendimento informando data, hotel, horários e o caso/INC (opcional).
3. Na aba **"📋 Histórico"**, visualize, edite ou exclua registros. Administradores e Gestores podem filtrar por plantonista.
4. Na sidebar, selecione o **mês, ano e colaborador** e clique em **"🚀 Gerar PDF"** para baixar a Folha de Hora Extra.
5. Administradores podem gerenciar hotéis e usuários nas abas **"🏨 Hotéis"** e **"⚙️ Usuários"**, e aprovar solicitações na aba **"🔔 Aprovações"**.

---

## Autor

Desenvolvido por **Caique Novaes**

- E-mail: [caiquenovaes1994@gmail.com](mailto:caiquenovaes1994@gmail.com)
- GitHub: [@caiquenovaes1994](https://github.com/caiquenovaes1994)

---

Desenvolvido com ☕ e Python · 2026
