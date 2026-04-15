"""
migrate_sqlite_to_pg.py
───────────────────────────────────────────────────────────────────────────────
Script utilitário para migrar dados do banco SQLite local para o PostgreSQL
no Supabase. Transfere todas as tabelas preservando tokens Fernet e hashes
Bcrypt intactos.

Uso:
    1. Configure as variáveis DB_* no seu .env
    2. Execute: python migrate_sqlite_to_pg.py
    3. Verifique os dados no Supabase Dashboard

ATENÇÃO: Este script NÃO apaga dados existentes no PostgreSQL.
         Ele usa ON CONFLICT para evitar duplicatas de hotéis e usuários.
         Chamados e solicitações são inseridos sem verificação de duplicata.
───────────────────────────────────────────────────────────────────────────────
"""
import os
import sys
import sqlite3

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ── Configuração ──────────────────────────────────────────────────────────────
SQLITE_DB = os.path.join("data", "horas_extras.db")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_pg_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require",
        options="-c search_path=public",
    )


def migrate():
    if not os.path.exists(SQLITE_DB):
        print(f"[ERRO] Arquivo SQLite não encontrado: {SQLITE_DB}")
        sys.exit(1)

    print(f"[INFO] Conectando ao SQLite: {SQLITE_DB}")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_cur = sqlite_conn.cursor()

    print(f"[INFO] Conectando ao PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    pg_conn = get_pg_conn()
    pg_cur = pg_conn.cursor()

    try:
        # ── 1. Migrar Usuários ────────────────────────────────────────────
        print("\n[1/4] Migrando USUARIOS...")
        sqlite_cur.execute(
            "SELECT username, password, nome_completo, is_admin, perfil, "
            "must_change_password, valor_base FROM usuarios"
        )
        users = sqlite_cur.fetchall()
        migrated = 0
        for row in users:
            username, password, nome, is_admin, perfil, must_change, valor_base = row
            try:
                pg_cur.execute(
                    "INSERT INTO usuarios (username, password, nome_completo, is_admin, perfil, must_change_password, valor_base) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                    "ON CONFLICT (username) DO UPDATE SET "
                    "password = EXCLUDED.password, nome_completo = EXCLUDED.nome_completo, "
                    "is_admin = EXCLUDED.is_admin, perfil = EXCLUDED.perfil, "
                    "must_change_password = EXCLUDED.must_change_password, valor_base = EXCLUDED.valor_base",
                    (username, password, nome, bool(is_admin), perfil or 'USER', bool(must_change), valor_base or '0.0')
                )
                migrated += 1
            except Exception as e:
                print(f"  [WARN] Erro ao migrar usuário '{username}': {e}")
                pg_conn.rollback()
        pg_conn.commit()
        print(f"  [OK] {migrated}/{len(users)} usuarios migrados.")

        # ── 2. Migrar Hotéis ──────────────────────────────────────────────
        print("\n[2/4] Migrando HOTEIS...")
        sqlite_cur.execute("SELECT rid, nome FROM hoteis WHERE rid IS NOT NULL AND rid != ''")
        hoteis = sqlite_cur.fetchall()
        migrated = 0
        for rid, nome in hoteis:
            try:
                pg_cur.execute(
                    "INSERT INTO hoteis (rid, nome) VALUES (%s, %s) ON CONFLICT (rid) DO NOTHING",
                    (rid, nome)
                )
                migrated += 1
            except Exception as e:
                print(f"  [WARN] Erro ao migrar hotel '{rid}': {e}")
                pg_conn.rollback()
        pg_conn.commit()
        print(f"  [OK] {migrated}/{len(hoteis)} hoteis migrados.")

        # ── 3. Migrar Chamados ────────────────────────────────────────────
        print("\n[3/4] Migrando CHAMADOS...")

        # Detectar colunas disponíveis no SQLite (compatibilidade com schemas antigos)
        sqlite_cur.execute("PRAGMA table_info(chamados)")
        cols_info = {row[1] for row in sqlite_cur.fetchall()}

        select_cols = ["data", "caso", "pms", "hotel", "inicio", "termino", "observacoes"]
        if "motivo" in cols_info:
            select_cols.append("motivo")
        if "username" in cols_info:
            select_cols.append("username")
        if "valor_base_snapshot" in cols_info:
            select_cols.append("valor_base_snapshot")

        sqlite_cur.execute(f"SELECT {', '.join(select_cols)} FROM chamados")
        chamados = sqlite_cur.fetchall()
        migrated = 0
        for row in chamados:
            row_dict = dict(zip(select_cols, row))
            try:
                pg_cur.execute(
                    "INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes, motivo, username, valor_base_snapshot) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        row_dict.get("data"),
                        row_dict.get("caso", ""),
                        row_dict.get("pms", ""),
                        row_dict.get("hotel", ""),
                        row_dict.get("inicio", ""),
                        row_dict.get("termino", ""),
                        row_dict.get("observacoes"),
                        row_dict.get("motivo", ""),
                        row_dict.get("username"),
                        row_dict.get("valor_base_snapshot", "0.0"),
                    )
                )
                migrated += 1
            except Exception as e:
                print(f"  [WARN] Erro ao migrar chamado: {e}")
                pg_conn.rollback()
        pg_conn.commit()
        print(f"  [OK] {migrated}/{len(chamados)} chamados migrados.")

        # ── 4. Migrar Solicitações de Hotéis ──────────────────────────────
        print("\n[4/4] Migrando SOLICITACOES_HOTEIS...")
        try:
            sqlite_cur.execute("SELECT rid, nome, tipo, user_id, status FROM solicitacoes_hoteis")
            sols = sqlite_cur.fetchall()
            migrated = 0
            for rid, nome, tipo, user_id, status in sols:
                try:
                    pg_cur.execute(
                        "INSERT INTO solicitacoes_hoteis (rid, nome, tipo, user_id, status) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (rid, nome, tipo, user_id, status)
                    )
                    migrated += 1
                except Exception as e:
                    print(f"  [WARN] Erro ao migrar solicitacao: {e}")
                    pg_conn.rollback()
            pg_conn.commit()
            print(f"  [OK] {migrated}/{len(sols)} solicitacoes migradas.")
        except sqlite3.OperationalError:
            print("  [INFO] Tabela solicitacoes_hoteis nao encontrada no SQLite. Pulando.")

        print("\n" + "=" * 60)
        print("MIGRACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        print("\nVerifique os dados no Supabase Dashboard - Table Editor.")

    except Exception as e:
        pg_conn.rollback()
        print(f"\n[ERRO FATAL] {e}")
        sys.exit(1)
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
