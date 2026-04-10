# Controle de Horas Extras 🕒

Sistema profissional desenvolvido em Python para gestão de atendimentos e controle rigoroso de horas extras, com geração de relatórios PDF de alta fidelidade técnica.

## 🚀 Funcionalidades

- **Autenticação Segura**: Sistema multiusuário com hashing de senha (SHA-256) e troca obrigatória de senha no primeiro acesso.
- **Gestão Inteligente**:
  - Cadastro e edição de Hotéis/PMS via janelas modais (`st.dialog`).
  - Gestão de Usuários (CRUD completo) para administradores.
  - Sincronização dinâmica com bases de dados externas.
- **Entrada de Dados Ágil**:
  - Máscara automática de horários (ex: ao digitar `0730` o sistema converte para `07:30`).
  - Campo de Caso/INC opcional.
- **Relatórios PDF Premium**:
  - Calendário completo de 26 a 25 (exibe todos os dias do período).
  - Destaque automático (fundo cinza) para Sábados, Domingos e Feriados.
  - Ajuste inteligente para caber em uma única página A4.
  - Cabeçalhos personalizados com cores corporativas.

## 🛠️ Tecnologias

- **Linguagem**: [Python](https://www.python.org/)
- **Interface**: [Streamlit](https://streamlit.io/)
- **Banco de Dados**: SQLite
- **Geração de PDF**: [ReportLab](https://www.reportlab.com/)

## 📦 Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/cnovaes/HorasExtras.git
   cd HorasExtras
   ```

2. **Execute o script de inicialização**:
   Basta executar o arquivo `start.bat`. Ele cuidará da criação do ambiente virtual (`venv`), instalação de dependências e execução do servidor.

   ```powershell
   ./start.bat
   ```

3. **Acesse no navegador**:
   O sistema estará disponível em: `http://localhost:3003`

---
**Desenvolvido por Caique Novaes**
