# Release Notes - HorasExtras

## [v2.0.3] - 2026-06-08

### Melhorias de UI (v2.0.3)

- **Página Dedicada de Histórico:** Criação de uma nova página `/changelog` para exibir o histórico completo de versões do sistema.
- **Botão de Versão Interativo:** O indicador de versão na barra lateral (sidebar) foi convertido em um botão interativo (`rx.button`) com contorno verde, servindo como atalho de navegação rápida para a página de histórico de versões. O `README.md` foi enxugado removendo a tabela de histórico obsoleta.

## [v2.0.2] - 2026-06-08

### Correções de Bugs (v2.0.2)

- **Porta Dinâmica no Deploy (Render):** Correção no parâmetro de porta (substituição de `port` por `frontend_port` no `rxconfig.py`), permitindo que a aplicação em modo *single port* utilize dinamicamente a porta definida pela variável de ambiente (`$PORT`) injetada pelo provedor de nuvem (Render), solucionando os erros de timeout ("No open ports detected").
- **Falha no Relatório Consolidado (Equipe):** Corrigido erro estrutural onde a geração do PDF consolidado falhava ao tentar extrair dados diretamente do modelo `Chamado` que na verdade pertenciam ao modelo `Usuario`. O processo foi refatorado para realizar o cruzamento correto de dados.
- **Valores a Receber (PDF):** Corrigida falha no cálculo financeiro dentro dos relatórios PDF. O valor capturado no snapshot estava sendo passado cifrado, causando falha de conversão e zerando os ganhos de horas 50% e 100%. Adicionada a rotina de descriptografia pré-processamento.

## [v2.0.1] - 2026-06-06

### Correções de Bugs (v2.0.1)

- **Supabase Auto-Migração:** Implementado script robusto de auto-migração (`apply_supabase_migrations`) para garantir a consistência dos dados em nuvem. Correção do erro fatal de tipagem (`operator does not exist: text >= date`) durante o deploy no Render, originado de bancos de dados legados exportados em SQLite. As colunas como `chamados.data` e booleanos são agora convertidas internamente antes da aplicação iniciar.
- **Criptografia do Valor Base:** Corrigida falha no registro de novos chamados onde o `valor_base_snapshot` não estava sendo salvo com a criptografia, deixando as informações de valores base financeiros visíveis como texto puro no Supabase.
- **Erros Silenciosos de Deleção:** Modificado o método de exclusão em massa (`DataState.bulk_delete`) para incluir tratamento explícito de exceções e alertas interativos ao usuário final (`rx.window_alert`). O usuário agora será notificado exatamente do porquê uma deleção falhou ao invés de receber alertas genéricos na UI, ajudando o suporte técnico.

### Melhorias de UI (v2.0.1)

- **Componente de Hotéis:** Atualizado o componente de seleção de hotéis no formulário de Criação/Edição de chamados. A combobox nativa (`datalist`) do navegador foi substituída pelo componente unificado `rx.select`, equalizando seu design visual e cores ao estilo escuro dos demais filtros de tela (Mês, Ano, Plantonista).
- **Rodapé de Versão:** A interface do usuário foi devidamente atualizada para refletir a versão da release atual (v2.0.1).
