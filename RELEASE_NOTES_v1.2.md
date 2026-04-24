# Release Notes — v1.2.0

> **Controle de Horas Extras**
> Lançamento: Abril de 2026

---

## Visão Geral

A versão **1.2.0** foca em **segurança e conformidade de acesso** no módulo de relatórios. O principal entregável é a implementação de uma *Trava de Segurança* em duas camadas — interface e banco de dados — que garante que um usuário de perfil comum nunca consiga acessar ou emitir relatórios de outros colaboradores, mesmo em tentativas de manipulação da UI. Adicionalmente, o relatório consolidado foi reestruturado e os perfis GESTOR/ADMIN recebem uma experiência de geração de PDF mais clara e direta.

---

## Novidades

### 🔒 Security Lock — Trava de Segurança em Relatórios

**Problema anterior:** A restrição de acesso existia apenas na interface. Um usuário com perfil `USER` poderia, teoricamente, contornar a UI e acionar queries sem filtro de username.

**Solução implementada:**

A proteção agora opera em **duas camadas independentes**:

**Camada 1 — Interface (`app.py`):**

- O seletor de colaboradores foi **removido completamente** para usuários com perfil `USER` na seção de relatórios da sidebar.
- O relatório é gerado automaticamente para o próprio usuário logado, sem qualquer input adicional necessário.
- O mesmo isolamento se aplica à aba **"📋 Histórico"**: usuários `USER` não visualizam o filtro de plantonistas.

**Camada 2 — Banco de Dados (`database.py`):**

- A função `get_all_chamados` recebeu dois novos parâmetros: `perfil` e `logged_username`.
- Quando `perfil == 'USER'`, a query **ignora o parâmetro `username_filter`** (que poderia ser injetado) e substitui pelo `logged_username` da sessão autenticada.
- Resultado: a query SQL sempre contém `WHERE username = %s` para usuários comuns, independente do que for passado pela interface.

---

### 📊 Relatório Consolidado

- A opção anteriormente chamada de **"TODOS"** foi renomeada para **"Consolidado"** no seletor de colaboradores da sidebar.
- A renomeação elimina ambiguidade semântica: a opção gera um PDF com **todos os colaboradores que tiveram registros no período**, não filtra "nenhum".
- Disponível exclusivamente para perfis **GESTOR** e **ADMIN**.

---

### 🛠️ Melhorias Técnicas

**Refatoração do cache de chamados:**

- A função `get_cached_chamados` foi atualizada para aceitar os parâmetros `perfil` e `logged_username`, propagando-os ao banco de dados.
- O cache `@st.cache_data` (TTL: 5 min) agora considera esses parâmetros na chave de cache, evitando colisões entre sessões de usuários diferentes.

**Sidebar — versão atualizada:**

- O número de versão exibido no rodapé da sidebar foi atualizado de `v1.1.0` para `v1.2.0`.

---

## Arquivos Modificados

| Arquivo | Tipo de alteração |
| :--- | :--- |
| `app.py` | Lógica da sidebar (relatório por perfil), seletor "Consolidado", repasse de parâmetros de segurança, versão no rodapé |
| `database.py` | Trava de segurança na função `get_all_chamados` (validação de perfil na camada de dados) |
| `README.md` | Atualização completa: matriz de permissões, seção de uso por perfil, histórico de versões, estrutura do projeto |
| `RELEASE_NOTES_v1.2.md` | Criado — documento de notas de versão |

---

## Compatibilidade

- ✅ Sem quebra de API — os parâmetros novos em `get_all_chamados` são opcionais com valor padrão `None`.
- ✅ Sem alteração de schema no banco de dados — nenhuma migração necessária.
- ✅ Compatível com dados de versões anteriores (v1.0.0 e v1.1.0).

---

## Versão Anterior

[v1.1.0] — Pool de conexões PostgreSQL (`psycopg2`), snapshot salarial cifrado por registro, exclusão em massa com confirmação modal, backup CSV automático com rotação.

---

Desenvolvido por Caique Novaes · 2026
