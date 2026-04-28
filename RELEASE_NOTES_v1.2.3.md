# Notas de Lançamento - v1.2.3

## Estabilização Pós-Migração (Ohio)

Esta versão consolida a migração da infraestrutura do banco de dados para a região **Ohio (us-east-2)**, garantindo melhor performance, menor latência e maior resiliência para o sistema de Controle de Horas Extras.

## O que há de novo

* **Novo Motor de Cálculo de Duração**:
  * Refatoração na função de agrupamento para converter horários (`HH:MM`) em `pd.to_timedelta`.
  * Implementação da lógica de módulo `(termino - inicio) % pd.Timedelta(days=1)` para calcular corretamente jornadas que cruzam a meia-noite.
  * Agregação explícita com `.agg({'duracao_td': 'sum'})` eliminando erros de `KeyError`.
  * Tratamento robusto para evitar quebras com registros nulos ou vazios vindos da base.
* **Automação de Fuso Horário (Brasília)**:
  * Integração com a biblioteca `pytz` para capturar a data/hora oficial de Brasília (`America/Sao_Paulo`).
  * Dashboard e filtros de PDF passam a abrir automaticamente no mês e ano correntes.
