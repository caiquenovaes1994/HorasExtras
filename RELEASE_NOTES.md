# Release Notes - HorasExtras

## [v2.0.1] - 2026-06-06

### Correções de Bugs (Bug Fixes)

- **Supabase Auto-Migração:** Implementado script robusto de auto-migração (`apply_supabase_migrations`) para garantir a consistência dos dados em nuvem. Correção do erro fatal de tipagem (`operator does not exist: text >= date`) durante o deploy no Render, originado de bancos de dados legados exportados em SQLite. As colunas como `chamados.data` e booleanos são agora convertidas internamente antes da aplicação iniciar.
- **Criptografia do Valor Base:** Corrigida falha no registro de novos chamados onde o `valor_base_snapshot` não estava sendo salvo com a criptografia, deixando as informações de valores base financeiros visíveis como texto puro no Supabase.
- **Erros Silenciosos de Deleção:** Modificado o método de exclusão em massa (`DataState.bulk_delete`) para incluir tratamento explícito de exceções e alertas interativos ao usuário final (`rx.window_alert`). O usuário agora será notificado exatamente do porquê uma deleção falhou ao invés de receber alertas genéricos na UI, ajudando o suporte técnico.

### Melhorias de UI (UI Enhancements)

- **Componente de Hotéis:** Atualizado o componente de seleção de hotéis no formulário de Criação/Edição de chamados. A combobox nativa (`datalist`) do navegador foi substituída pelo componente unificado `rx.select`, equalizando seu design visual e cores ao estilo escuro dos demais filtros de tela (Mês, Ano, Plantonista).
- **Rodapé de Versão:** A interface do usuário foi devidamente atualizada para refletir a versão da release atual (v2.0.1).
