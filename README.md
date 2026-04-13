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

- Segurança rigorosa nos logs com algoritmos **hash bcrypt** (senha) escaláveis.
- Proteção nativa de informações sensíveis (como salários base) por **Criptografia Simétrica (AES / Fernet)** para adequações diretas de LGPD.
- Distinção em operações entre perfis de **Administrador** da plataforma e **Usuário comum**.
- **Troca de Senha Obrigatória** disparada nativamente no início de sessão de novos convidados/colegas na plataforma.

### Gestão de Hotéis / PMS

- Cadastro e edição de hotéis via **janela modal** (`st.dialog`)
- **Base Externa Opcional:** O sistema referencia um arquivo `data/hotels_source.sqlite` para carregar clientes massificados. Caso o arquivo não exista após o clone, o sistema opera 100% de maneira autônoma com seus hotéis inseridos manualmente.
- Garantia de registros únicos com `SELECT DISTINCT` (sem duplicações)

### Gestão de Usuários (Admin)

- **CRUD completo** de usuários em interface modal dedicada
- Definição de perfil administrador diretamente na criação

### Trava de Base Financeira (Salário)

- **Captura via Snapshot:** Salários diários são individualmente capturados de forma cifrada atrelados a cada entrada gerada pelo colaborador.  
- **Redução de Impacto de Ajuste:** Reajustes salariais (aumentos e dissídios) de perfil em tempo-real não afetam a emissão e integridade PDF calculada de meses anteriores do histórico de remuneração.

### Registro de Atendimentos

- Máscara de horário automática (ex: digitando `0730` → converte para `07:30`)
- Campo Caso/INC **opcional**
- Seleção dinâmica de Hotel/PMS populada diretamente do banco de dados

### Relatório PDF de Alta Fidelidade

- **Calendário completo**: exibe todos os dias do período (26 do mês anterior ao 25 do mês atual), mesmo os sem registro
- Destaque automático com **fundo cinza (#D3D3D3)** em Sábados, Domingos e Feriados
- Cálculo automático de faturamento iterado (linha a linha) baseando-se nas regras de divisores legais para horas de **50%** (dias úteis e sábados) e **100%** (domingos e feriados).
- Ajuste automático para caber em **uma única página A4**
- Cabeçalho profissional com destaque em cor vinho corporativa

## Tecnologias

| Tecnologia | Versão | Finalidade |
| :--- | :--- | :--- |
| [Python](https://python.org) | 3.12 | Linguagem principal |
| [Streamlit](https://streamlit.io) | 1.56 | Interface web |
| [SQLite](https://sqlite.org) | — | Banco de dados local |
| [ReportLab](https://reportlab.com) | — | Geração de relatórios PDF |
| [Pandas](https://pandas.pydata.org) | — | Manipulação de dados |
| [holidays](https://pypi.org/project/holidays/) | — | Detecção de feriados nacionais (BR) |

---

## Estrutura do Projeto

```text
HorasExtras/
│
├── app.py               # Interface principal (Streamlit)
├── database.py          # Camada de acesso ao banco de dados (CRUD)
├── report_generator.py  # Geração de relatórios em PDF (ReportLab)
├── utils.py             # Funções auxiliares (cálculos, máscaras, período)
│
├── data/                # Diretório de dados locais (ignorado pelo Git)
│   └── horas_extras.db  # Banco de dados principal (SQLite)
│
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

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves de ambiente vitais:

```env
SECRET_KEY=sua_chave_fernet_aqui
ADMIN_PWD=sua_senha_admin_inicial
```

> **Nota:** A `SECRET_KEY` deve ser obrigatoriamente um token de 32 bytes extraído via algoritmo AES suportado pelo módulo de encriptação Python local.

#### 3. Execute o script de inicialização

O arquivo `start.bat` automatiza todo o processo: cria o ambiente virtual, instala as dependências e inicia o servidor.

```powershell
./start.bat
```

#### 4. Acesse a aplicação no navegador

```text
http://localhost:3003
```

> **Login padrão (primeiro acesso):** Utilize as credenciais de administrador fornecidas pelo gestor do sistema.

---

## Uso

1. **Faça login** com as suas credenciais.
2. Na aba **"📝 Novo Registro"**, registre o atendimento informando data, hotel, horários e o caso/INC (opcional).
3. Na sidebar, selecione o **mês e ano** e clique em **"🚀 Gerar PDF"** para baixar a Folha de Hora Extra.
4. Administradores podem gerenciar hotéis e usuários via CRUD no menu lateral.

---

## Autor

Desenvolvido por **Caique Novaes**

- E-mail: [caiquenovaes1994@gmail.com](mailto:caiquenovaes1994@gmail.com)
- GitHub: [@caiquenovaes1994](https://github.com/caiquenovaes1994)

---

Desenvolvido com ☕ e Python · 2026
