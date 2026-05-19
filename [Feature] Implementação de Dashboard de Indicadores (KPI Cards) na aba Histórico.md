# Implementação de Dashboard de Indicadores (KPI Cards) na aba Histórico

## Descrição

Implementar uma seção de **resumo estatístico** no topo da aba **"Histórico"** para fornecer insights imediatos sobre a competência selecionada, antes da listagem detalhada de chamados.

---

## Componentes a serem adicionados

| # | Card | Descrição |
| - | ---- | --------- |
| 1 | **Total de Horas (50% e 100%)** | Exibição segregada das horas trabalhadas por tipo de adicional. |
| 2 | **Ganhos Estimados** | Cálculo em tempo real do valor a receber, utilizando a lógica de descriptografia do `valor_base`. |
| 3 | **Contador de Chamados** | Total de registros presentes no filtro atual. |
| 4 | **Média / Chamado** | Cálculo da duração média dos atendimentos (`Duração Total / Quantidade`). |

---

## Mockup da Disposição

```text
┌──────────────┬──────────────┬──────────────┬──────────────┐
│  🕐 Horas    │  💰 Ganhos   │  📋 Total    │  📊 Média    │
│   50% / 100% │  Estimados   │  Chamados    │  / Chamado   │
│              │              │              │              │
│  12h30 / 8h  │  R$ 1.250,00 │     42       │   0h29min    │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## Requisitos Técnicos (Streamlit)

- [x] Utilizar `st.columns(4)` para a disposição horizontal dos cards.
- [x] Integrar com as funções de cálculo do `utils.py` para garantir que a lógica de **"virada de meia-noite"** seja respeitada.
- [x] As métricas devem reagir **instantaneamente** aos filtros de pesquisa e competência.
- [x] Utilizar `st.metric()` para exibição dos valores com suporte a `delta` (variação em relação à competência anterior, se aplicável).

---

## Critérios de Aceite

- [x] Os 4 cards são renderizados corretamente no topo da aba Histórico.
- [x] Os valores de horas 50% e 100% são calculados de forma segregada e precisa.
- [x] O cálculo de ganhos estimados utiliza a descriptografia do `valor_base` sem expor dados sensíveis.
- [x] O contador reflete o total de registros **após** a aplicação de todos os filtros ativos.
- [x] A média por chamado é calculada considerando a lógica de virada de meia-noite.
- [x] A atualização dos cards é reativa — qualquer alteração de filtro ou competência atualiza os valores imediatamente.

---
