# Release Notes — v1.2.1

> **Controle de Horas Extras**
> Hotfix · Lançamento: Abril de 2026

---

## Visão Geral

A **v1.2.1** é um hotfix crítico de segurança. Foi identificado em produção que o *Security Lock* introduzido na v1.2.0 possuía uma falha: quando o parâmetro de filtro chegava nulo à camada de banco de dados, o sistema executava uma query sem cláusula `WHERE`, expondo registros de todos os colaboradores a usuários com perfil `USER`.

Esta versão corrige a falha com travas redundantes em duas camadas — interface e banco de dados — e normaliza o tratamento de perfis para evitar inconsistências de caixa ou espaços vindos da sessão.

---

## Correções

### 🔒 Reforço do Security Lock

**Problema:** A função `get_all_chamados` em `database.py` possuía um bloco `else` que executava uma query sem filtro `WHERE` quando `final_username` era nulo. Isso ocorria quando `logged_username` não estava presente na sessão, fazendo o sistema cair no fallback e retornar todos os registros.

**Solução — Camada de Banco de Dados (`database.py`):**

- Adicionada normalização rigorosa do perfil no início da função:

  ```python
  perfil_norm = str(perfil).strip().upper() if perfil else 'USER'
  ```

- Se `perfil_norm == 'USER'`, o filtro é forçado a ser o `logged_username`, sem exceção.

- Implementada **Trava de Segurança Final**: se o filtro resultante for nulo e o perfil não for `ADMIN` ou `GESTOR`, a função retorna `[]` imediatamente — a query nunca é executada.

- O bloco `else` (query sem `WHERE`) passa a ser alcançável **somente** por `ADMIN` e `GESTOR` para o relatório Consolidado.

**Solução — Camada de Interface (`app.py`):**

- No `TAB_HIST`, a variável `username_filter` é inicializada diretamente com o username da sessão para perfis `USER`, antes de qualquer outra lógica de filtragem:

  ```python
  username_filter = st.session_state.user["username"] if u_perfil == "USER" else None
  ```

- O perfil é normalizado com `.strip().upper()` em todos os pontos de leitura da sessão (sidebar e corpo principal).

### 🛠️ Melhorias Técnicas

- **Garantia de Tipagem:** Reforçada a conversão de datas retornadas pelo PostgreSQL para string `YYYY-MM-DD`, prevenindo erros de renderização no `st.dataframe`.
- **Normalização Global de Perfil:** Aplicado `.strip().upper()` em todas as leituras de `st.session_state.user["perfil"]` para imunizar contra inconsistências de caixa ou espaços na sessão.

---

## Arquivos Modificados

| Arquivo | Alteração |
| :--- | :--- |
| `database.py` | Normalização de perfil + trava contra fallback geral em `get_all_chamados` |
| `app.py` | Normalização de perfil em dois pontos + trava estrita no `TAB_HIST` + versão `v1.2.1` no rodapé |
| `README.md` | Badge de versão, histórico de versões, estrutura do projeto e link de release notes atualizados |

---

## Compatibilidade

- ✅ Totalmente compatível com dados das versões 1.0.0, 1.1.0 e 1.2.0.
- ✅ Sem alterações de schema — nenhuma migração de banco de dados necessária.
- ✅ Sem quebra de API — os parâmetros de `get_all_chamados` permanecem os mesmos.

---

## Versão Anterior

[v1.2.0] — Security Lock inicial em duas camadas, seletor "Consolidado" para Gestor/Admin, refatoração de cache.

---

Desenvolvido por Caique Novaes · 2026
