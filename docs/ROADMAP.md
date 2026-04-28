# Plano de Evolução e Roadmap do Projeto

Este documento contém os rascunhos para as próximas atualizações e melhorias estratégicas do sistema de Horas Extras.

---

## 1. Issue: Implementação de Aceite de Termos de Uso (LGPD) ⚖️

**Descrição:** Para garantir a transparência no tratamento de dados e definir as responsabilidades entre o desenvolvedor e o usuário, este ticket visa implementar um fluxo de aceite obrigatório de Termos de Uso. O sistema armazena informações sensíveis (salários e horas), portanto, é necessário formalizar o consentimento de acordo com a LGPD.

### 📋 Critérios de Aceite

#### 🗄️ Alteração no Schema do Banco de Dados (`database.py`)

- [ ] Adicionar coluna `aceitou_termos` (boolean, default: `False`) na tabela `usuarios`.
- [ ] Adicionar coluna `data_aceite` (timestamp) para registro de auditoria e conformidade.

#### 🛡️ Gatekeeper de Login (`app.py`)

- [ ] Implementar validação no fluxo de autenticação para verificar se o usuário logado já aceitou os termos.
- [ ] Caso `aceitou_termos == False`, bloquear o acesso ao dashboard e exibir um modal obrigatório.

#### 💻 Interface de Aceite (Streamlit)

- [ ] Criar modal/tela de termos com `st.expander` para leitura integral do texto.
- [ ] Adicionar `st.checkbox` obrigatório ("Li e concordo com os termos").
- [ ] O botão de "Concluir/Acessar" deve permanecer desabilitado até que o checkbox seja marcado.
- [ ] Ao aceitar, atualizar o banco de dados with `True` e a data/hora atual.

#### 📄 Documentação e Acessibilidade

- [ ] Disponibilizar os termos para visualização constante na aba **"Perfil"**.
- [ ] Implementar funcionalidade de exportação/download dos termos em formato **PDF** dentro do perfil.

**Etiquetas Sugeridas:** `feature`, `security`, `legal/LGPD`

---

## 2. Issue: [ROADMAP / LONGO PRAZO] Migração do Frontend para Reflex (Python Full-Stack) 🚀

**Descrição:** Esta é uma iniciativa estratégica para a evolução tecnológica do projeto. O objetivo central é substituir o **Streamlit** pelo **Reflex**, permitindo um nível de personalização visual, controle de estado e performance superior, mantendo o ecossistema 100% em **Python 3.12**.

### 🎯 Motivação

- **Customização UI/UX:** Superar as limitações de layout do Streamlit, permitindo a criação de uma interface moderna e exclusiva, alinhada à identidade visual de sistemas corporativos (ex: Accor/Opera Cloud).
- **Performance em Escala:** O Reflex utiliza uma arquitetura baseada em Next.js no frontend e FastAPI no backend, lidando de forma mais eficiente com múltiplos usuários simultâneos e estados de sessão complexos.
- **Profissionalismo Comercial:** Preparar a robustez do software para a comercialização oficial via Microempresa (ME) planejada para o **Q2 2026**.

### 🏗️ Escopo Técnico Estimado

#### ✅ O que será Preservado

- **Backend de Dados:** O arquivo `database.py` e toda a lógica de integração com o **Supabase** serão mantidos.
- **Lógica de Negócio:** Os cálculos de horas extras e regras de validação permanecem em Python.

#### 🛠️ O que será Implementado

- **Refatoração Completa do Frontend:** Substituição do `app.py` por uma estrutura baseada em componentes **Reflex** e **Radix UI**.
- **Design Responsivo (Mobile Friendly):** Implementação de layouts que se adaptam perfeitamente a smartphones e tablets.

**Status:** 🟡 Backlog (Long-term)
**Etiquetas Sugeridas:** `roadmap`, `frontend`, `python-fullstack`, `future-idea`
