# Release Notes - v1.4.1 (Junho 2026)

## 🐛 Correções de Bugs (Bug Fixes)

* **Feriados Móveis (Corpus Christi e Carnaval):** Corrigido o cálculo de feriados no sistema que utilizava apenas a lista de feriados fixos da biblioteca `holidays`. Como o Corpus Christi e o Carnaval são datas móveis (dependentes da Páscoa), foi implementado o cálculo dinâmico utilizando `dateutil.easter`, garantindo que essas datas passem a ser consideradas como `FERIADO` (ou ponto facultativo) e pontuadas como 100% nas horas extras para a cidade de São Paulo.
* **Alertas de Linter (Tipagem e Sintaxe):**
  * Atualizada a chamada da biblioteca `holidays` de `holidays.Brazil(state="SP")` para o padrão mais recente `holidays.country_holidays("BR", subdiv="SP")`.
  * Corrigida a inferência de tipo na aplicação da função `formatar_timedelta` à coluna `duracao_td`, evitando avisos incorretos do linter na IDE.

## 💄 Melhorias de UI (UI Improvements)

* **Sidebar:** O texto de rodapé da barra lateral ("Desenvolvido por Caique Novaes..." e o versionamento) foi centralizado para melhor harmonia visual.
