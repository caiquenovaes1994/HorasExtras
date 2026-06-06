# ✅ Roadmap de Migração: Streamlit ➔ Reflex — **CONCLUÍDO na v2.0.0**

Este documento estabelece o plano de engenharia passo a passo para migrar o ecossistema do Controle de Horas Extras do Streamlit para a arquitetura reativa e full-stack do Reflex. A migração ocorrerá de forma totalmente isolada em um diretório de backup (Sandbox), mantendo a versão v1.4.1 em produção intocada.

## 📅 Visão Geral do Cronograma

| Fase | Escopo Principal | Complexidade | Módulos Impactados |
| :--- | :--- | :--- | :--- |
| **Fase 1** | Autenticação Segura e Cookies Nativos | Média | `state.py`, `database.py` |
| **Fase 2** | Sincronização Assíncrona com Supabase Ohio | Média | `models.py`, `state.py` |
| **Fase 3** | Motor de Regras de Negócio e Tempo (Pandas ➔ Vars) | Alta | `utils.py`, `state.py` |
| **Fase 4** | UI Dinâmica, Filtros e KPI Cards | Média | `HorasExtras_Reflex.py` |
| **Fase 5** | Desacoplamento do Gerador de PDF (ReportLab) | Alta | `report_generator.py` |
| **Fase 6** | Homologação Local e Validação de Dados | Baixa | Todo o ecossistema |

## 🏗️ Detalhamento das Etapas

### Fase 1: Autenticação Segura e Cookies Nativos

O objetivo é substituir o gerenciador de cookies de terceiros do Streamlit pelo sistema nativo de persistência do Reflex, mantendo os hashes de segurança.

- [x] **Configuração do Token de Sessão:** Implementar o armazenamento do token de login cifrado diretamente no `rx.Cookie` do Reflex, com expiração configurada para 24 horas.
- [x] **Integração Bcrypt/Fernet:** Conectar a função `State.login` às rotinas de checagem de senha (`_check_pw`) e decodificação do salário base definidas no `database.py`.
- [x] **Gate de Troca de Senha:** Implementar o desvio reativo para usuários com a flag `must_change_password = True` ativa.

### Fase 2: Sincronização Assíncrona com Supabase Ohio

Configurar a comunicação do backend do Reflex (FastAPI) com a infraestrutura de banco de dados ativa.

- [x] **Mapeamento SQLModel:** Garantir que as classes em `models.py` reflitam as restrições (`UNIQUE`) e tipos corretos de chaves primárias (`bigint`/`int8`) do Supabase.
- [x] **Queries Assíncronas:** Adaptar as buscas de chamados para rodar de forma não-bloqueante, evitando gargalos na interface gráfica quando múltiplos registros forem carregados.
- [x] **Persistência do Aceite (LGPD):** Validar a gravação imediata da flag `aceitou_termos` e do timestamp no fuso horário de Brasília (`America/Sao_Paulo`) no banco de dados.

### Fase 3: Motor de Regras de Negócio e Tempo

Migrar as funções matemáticas e de tratamento de feriados do modelo linear para o reativo.

- [x] **Portabilidade de Feriados:** Garantir que o cache de feriados móveis (como Carnaval e Corpus Christi) e municipais de São Paulo funcione de maneira síncrona dentro do ciclo de vida do Reflex.
- [x] **Cálculo de Duração Reativo:** Migrar a fórmula matemática de cruzamento de meia-noite `((termino - inicio) mod 24h)` para um método utilitário executado no backend do Reflex.
- [x] **Variáveis Computadas (`@rx.var`):** Transformar o agrupamento de horas em propriedades computadas na classe `State`, permitindo que os totais de 50% e 100% recalculem instantaneamente na tela ao alterar a competência.

### Fase 4: UI Dinâmica, Filtros e KPI Cards

Construir a experiência visual tridimensional e reativa na aba Histórico.

- [x] **Unificação dos Filtros:** Dispor os seletores de Plantonista, Mês e Ano em uma linha única horizontal utilizando o sistema de grid (`rx.hstack` ou `rx.grid`).
- [x] **KPI Cards:** Desenhar os 4 cartões de indicadores (Total de Horas, Ganhos Estimados, Total Chamados e Média) utilizando propriedades de estilo nativas do Reflex, eliminando a injeção de HTML/CSS.
- [x] **Tabela de Registros:** Implementar o componente `rx.table.root` integrado com checkboxes para a futura funcionalidade de exclusão em massa.

### Fase 5: Desacoplamento do Gerador de PDF

Isolar a biblioteca ReportLab para rodar sem interferir no servidor de interface do Reflex.

- [x] **Isolamento de Threads:** Como o ReportLab gera arquivos de forma síncrona, encapsular as funções `gerar_pdf` e `gerar_pdf_massa` dentro de decoradores `@rx.background` no Reflex, evitando travamentos na tela do usuário.
- [x] **Fluxo de Download:** Configurar o endpoint de download do Reflex para ler os bytes do PDF gerado e disponibilizá-los com segurança no navegador do usuário.

### Fase 6: Homologação Local e Validação de Dados

Garantir a paridade total de resultados antes de qualquer tomada de decisão sobre o projeto principal.

- [x] **Batimento de Relatórios:** Gerar o mesmo relatório de competência no Streamlit e no Reflex Sandbox, validando se os centavos dos Ganhos Estimados e as somas das horas fecham com precisão milimétrica.
- [x] **Validação de Bugs Ocultos:** Testar exaustivamente cenários críticos, como chamados com campos nulos ou formatações inválidas importadas do CSV.

## 🛑 Regras de Ouro para o Sandbox

- **Isolamento de Escrita:** Durante os testes na branch do Reflex, evite realizar operações de `DROP` ou `ALTER TABLE` no banco de dados que possam afetar a estrutura lida pela versão estável do Streamlit em produção.
- **Ambientes Virtuais Exclusivos:** Mantenha os arquivos de dependências separados para evitar que o ecossistema do Reflex interfira nos pacotes instalados no servidor do Render.
