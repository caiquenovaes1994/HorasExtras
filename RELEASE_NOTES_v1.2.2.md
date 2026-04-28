# Release Notes — v1.2.2

> **Controle de Horas Extras**
> Infraestrutura · Lançamento: Abril de 2026

---

## Visão Geral

A **v1.2.2** marca a conclusão bem-sucedida da migração da infraestrutura de banco de dados para a região de Ohio (us-east-2) no Supabase. Esta atualização foca na melhoria de desempenho, escalabilidade e manutenção da segurança rigorosa implementada nas versões anteriores.

---

## Ações Realizadas

### 🚀 Otimização de Latência

* **Migração de Região:** A base de dados foi movida para a região de Ohio (`us-east-2`), alinhando-se geograficamente com o servidor de hospedagem (Render).
* **Performance:** Eliminação do atraso transcontinental que ocorria anteriormente entre o Brasil e os EUA, resultando em consultas mais rápidas e uma experiência de usuário muito mais responsiva.
* **Novo Host do Pooler:** Atualizado para `aws-1-us-east-2.pooler.supabase.com` (porta `6543`).

### 📊 Upgrade de Dados e Escalabilidade

* **Chaves Primárias:** Conversão de todas as chaves primárias (`id`) de `int` para `bigint` (`int8`) nas tabelas do banco de dados.
* **Escalabilidade:** Esta alteração garante que o sistema suporte volumes massivos de registros sem risco de estouro de capacidade do identificador único.

### 🔒 Manutenção de Segurança

* **Garantia da v1.2.1:** Confirmado que todas as normalizações rigorosas de perfil (`perfil.upper()`) e as travas de segurança introduzidas no hotfix v1.2.1 permanecem 100% ativas e operacionais após a migração.
* Os dados migrados preservaram a integridade dos relacionamentos e permissões.

---

## Arquivos Modificados

| Arquivo | Alteração |
| :--- | :--- |
| `.env` | Atualização do host do banco de dados e ID do projeto para a nova região |
| `.env.example` | Documentação do novo host e padrão do ID do projeto |
| `app.py` | Atualização do número da versão no rodapé para `v1.2.2` |
| `README.md` | Atualização da tabela de histórico de versões para `v1.2.2` |

---

## Compatibilidade

* ✅ Totalmente compatível com as regras de negócio da v1.2.1.
* ⚠️ Requer atualização das variáveis de ambiente (`.env`) nos servidores locais e de produção.

---

## Versão Anterior

[v1.2.1] — Hotfix crítico de segurança, travamento de fallback para usuários comuns.

---

Desenvolvido por Caique Novaes · 2026
