# Notas de Lançamento - v1.3.1

## Ajustes de Interface (Patch)

### O que há de novo

* **Densidade de Filtros no Histórico**:
  * Os seletores de Plantonista, Mês e Ano foram unificados em uma única linha horizontal (`st.columns([2, 1, 1])`), reduzindo o espaço vertical consumido pelos filtros e melhorando a densidade de informações.
  * Usuários com perfil `USER` mantêm o layout de dois filtros (Mês e Ano) em linha única.

* **Correção de Glitch Visual no Cabeçalho do Histórico**:
  * Removido o `st.divider()` que aparecia fragmentado entre o cabeçalho da tabela de registros e a listagem, eliminando a linha visual indesejada à esquerda da coluna "Data".

* **Atualização de Versão**:
  * Rodapé da sidebar atualizado de `v1.3.0` para `v1.3.1`.

* **Manutenção do .gitignore**:
  * Adicionada a entrada `.vs/` para ignorar a pasta gerada pelo Visual Studio.
