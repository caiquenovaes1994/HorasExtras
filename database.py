import os
import csv
import glob
from datetime import datetime
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool, extras
import bcrypt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO E SEGURANÇA
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

# Conexão PostgreSQL (Supabase)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_PORT = os.getenv("DB_PORT", "5432")

# Diretórios locais para exportação CSV
EXPORT_DIR = os.path.join("data", "exports")

# Fonte externa SQLite para sincronização inicial de hotéis (fallback local)
EXTERNAL_SOURCE = os.path.join("data", "hotels_source.sqlite")

# Chave Secreta para Criptografia de Dados (Salários)
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_PWD  = os.getenv("ADMIN_PWD", "mudar123")

# Inicializa cifras apenas se a chave estiver presente
_cipher = Fernet(SECRET_KEY.encode()) if SECRET_KEY else None

# ─────────────────────────────────────────────────────────────────────────────
# CRIPTOGRAFIA — Fernet (AES) & Bcrypt
# ─────────────────────────────────────────────────────────────────────────────
def _encrypt(val: float) -> str:
    """Criptografa um valor numérico para armazenamento (AES)."""
    if not _cipher or val is None: return "0.0"
    token = _cipher.encrypt(str(val).encode())
    return token.decode()

def _decrypt(token: str) -> float:
    """Descriptografa um valor para uso em memória."""
    if not _cipher or not token or token == "0.0": return 0.0
    try:
        val = _cipher.decrypt(token.encode()).decode()
        return float(val)
    except:
        return 0.0

def encrypt_str(val: str) -> str:
    """Criptografa uma string pura."""
    if not _cipher or not val: return ""
    return _cipher.encrypt(val.encode()).decode()

def decrypt_str(token: str) -> str:
    """Descriptografa uma string pura."""
    if not _cipher or not token: return ""
    try:
        return _cipher.decrypt(token.encode()).decode()
    except:
        return ""

def _hash_pw(password: str) -> str:
    """Gera um hash seguro usando Bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def _check_pw(password: str, hashed: str) -> bool:
    """Verifica uma senha com Bcrypt."""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# POOL DE CONEXÕES — PostgreSQL
# ─────────────────────────────────────────────────────────────────────────────
_pool: pool.SimpleConnectionPool | None = None

def _init_pool():
    """Inicializa o pool de conexões PostgreSQL."""
    global _pool
    if _pool is None:
        _pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=5,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require",          # Supabase exige SSL
            connect_timeout=10,
            options="-c search_path=public",
        )

@contextmanager
def get_db():
    """Context manager que obtém uma conexão do pool e a devolve ao final.

    Faz commit automático em caso de sucesso e rollback em caso de exceção,
    garantindo que a conexão seja SEMPRE devolvida ao pool.
    """
    _init_pool()
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZAÇÃO E MIGRAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
def executar_backup_automatico():
    """Registra que o banco opera em nuvem e exporta CSVs locais como segurança extra.

    O Supabase já realiza backups automáticos diários. Esta função exporta as
    tabelas principais para arquivos CSV locais, mantendo no máximo 10 versões.
    """
    try:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        agora = datetime.now().strftime("%Y%m%d_%H%M%S")

        tabelas = {
            "chamados": "SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, username, valor_base_snapshot FROM chamados",
            "usuarios": "SELECT id, username, nome_completo, is_admin, perfil, must_change_password FROM usuarios",
        }

        with get_db() as conn:
            cur = conn.cursor()
            for tabela, query in tabelas.items():
                try:
                    cur.execute(query)
                    rows = cur.fetchall()
                    col_names = [desc[0] for desc in cur.description]

                    csv_path = os.path.join(EXPORT_DIR, f"{tabela}_{agora}.csv")
                    with open(csv_path, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(col_names)
                        writer.writerows(rows)
                except Exception as e:
                    print(f"[BACKUP CSV] Erro ao exportar '{tabela}': {e}")

        # Rotação: manter apenas os 10 exports mais recentes por tabela
        for tabela in tabelas:
            bkps = sorted(glob.glob(os.path.join(EXPORT_DIR, f"{tabela}_*.csv")))
            if len(bkps) > 10:
                for f in bkps[:-10]:
                    try: os.remove(f)
                    except: pass

        print(f"[BACKUP] Exportação CSV concluída em {agora}. Banco opera em nuvem (Supabase).")
    except Exception as e:
        print(f"[BACKUP] Erro no backup automático: {e}")




def init_db():
    """Cria as tabelas no PostgreSQL e executa migrações de schema."""
    with get_db() as conn:
        cur = conn.cursor()

        # ── Criação de Tabelas ────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id              SERIAL PRIMARY KEY,
                data            DATE        NOT NULL,
                caso            TEXT,
                pms             TEXT,
                hotel           TEXT,
                inicio          TEXT        NOT NULL,
                termino         TEXT        NOT NULL,
                observacoes     TEXT,
                motivo          TEXT,
                username        TEXT,
                valor_base_snapshot TEXT DEFAULT '0.0'
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS solicitacoes_hoteis (
                id      SERIAL PRIMARY KEY,
                rid     TEXT    NOT NULL,
                nome    TEXT    NOT NULL,
                tipo    TEXT    NOT NULL,
                user_id INTEGER,
                status  TEXT    DEFAULT 'PENDING'
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id                   SERIAL PRIMARY KEY,
                username             TEXT    UNIQUE NOT NULL,
                password             TEXT    NOT NULL,
                nome_completo        TEXT,
                is_admin             BOOLEAN DEFAULT FALSE,
                perfil               TEXT    DEFAULT 'USER',
                must_change_password BOOLEAN DEFAULT TRUE,
                valor_base           TEXT    DEFAULT '0.0'
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS hoteis (
                id   SERIAL PRIMARY KEY,
                rid  TEXT   UNIQUE,
                nome TEXT   NOT NULL
            )
        """)

        # ── Migrações (idempotentes com savepoints) ──────────────────────
        migrations = [
            ("usuarios", "perfil", "TEXT DEFAULT 'USER'"),
            ("chamados", "username", "TEXT"),
            ("usuarios", "valor_base_secure", "TEXT DEFAULT '0.0'"),
            ("chamados", "motivo", "TEXT"),
            ("chamados", "valor_base_snapshot", "TEXT DEFAULT '0.0'"),
        ]
        for table, column, col_type in migrations:
            try:
                cur.execute("SAVEPOINT sp_migration")
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
                cur.execute("RELEASE SAVEPOINT sp_migration")
            except psycopg2.errors.DuplicateColumn:
                cur.execute("ROLLBACK TO SAVEPOINT sp_migration")
                cur.execute("RELEASE SAVEPOINT sp_migration")

        # Sincroniza perfis antigos baseados em is_admin
        cur.execute("UPDATE usuarios SET perfil = 'ADMIN' WHERE is_admin = TRUE AND (perfil IS NULL OR perfil = 'USER')")

        # Atribui registros órfãos ao primeiro admin encontrado
        cur.execute("SELECT username FROM usuarios WHERE perfil = 'ADMIN' LIMIT 1")
        admin_row = cur.fetchone()
        if admin_row:
            cur.execute("UPDATE chamados SET username = %s WHERE username IS NULL", (admin_row[0],))

        # Admin padrão baseado no .env
        cur.execute("SELECT id FROM usuarios WHERE username = 'cnovaes'")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO usuarios (username, password, nome_completo, is_admin, perfil, must_change_password) "
                "VALUES ('cnovaes', %s, 'CAIQUE NOVAES', TRUE, 'ADMIN', FALSE)",
                (_hash_pw(ADMIN_PWD),)
            )

        # Hotel padrão
        cur.execute("INSERT INTO hoteis (rid, nome) VALUES ('B669', 'Ibis Caruaru') ON CONFLICT (rid) DO NOTHING")

    # Sincroniza hotéis externos (fallback local)
    with get_db() as conn2:
        cur2 = conn2.cursor()
        cur2.execute("SELECT COUNT(*) FROM hoteis")
        total = cur2.fetchone()[0]
    if total <= 1:
        _sync_hotels()


def _sync_hotels():
    """Importa hotéis de uma fonte SQLite externa (fallback local)."""
    if not os.path.exists(EXTERNAL_SOURCE):
        return
    try:
        import sqlite3
        ext = sqlite3.connect(EXTERNAL_SOURCE)
        rows = ext.execute("SELECT DISTINCT rid, nome FROM hotels WHERE rid IS NOT NULL AND rid != ''").fetchall()
        ext.close()

        with get_db() as conn:
            cur = conn.cursor()
            for rid, nome in rows:
                cur.execute(
                    "INSERT INTO hoteis (rid, nome) VALUES (%s, %s) ON CONFLICT (rid) DO NOTHING",
                    (rid, nome)
                )
    except Exception as e:
        print(f"[SYNC] Erro ao sincronizar hotéis: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# HOTÉIS E SOLICITAÇÕES
# ─────────────────────────────────────────────────────────────────────────────
def get_hoteis() -> list[tuple]:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT rid, nome FROM hoteis WHERE rid IS NOT NULL AND rid != '' ORDER BY rid ASC")
        return cur.fetchall()

def criar_solicitacao_hotel(rid: str, nome: str, tipo: str, user_id: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO solicitacoes_hoteis (rid, nome, tipo, user_id, status) VALUES (%s, %s, %s, %s, 'PENDING')",
            (rid, nome, tipo, user_id)
        )

def get_solicitacoes_pendentes() -> list[tuple]:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT s.id, s.rid, s.nome, s.tipo, u.nome_completo "
            "FROM solicitacoes_hoteis s LEFT JOIN usuarios u ON s.user_id = u.id "
            "WHERE s.status = 'PENDING'"
        )
        return cur.fetchall()

def processar_solicitacao(sid: int, aprovado: bool):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT rid, nome, tipo FROM solicitacoes_hoteis WHERE id = %s", (sid,))
        row = cur.fetchone()
        if row:
            rid, nome, tipo = row
            if aprovado:
                if tipo == 'CREATE':
                    cur.execute(
                        "INSERT INTO hoteis (rid, nome) VALUES (%s, %s) ON CONFLICT (rid) DO UPDATE SET nome = EXCLUDED.nome",
                        (rid, nome)
                    )
                elif tipo == 'EDIT':
                    cur.execute("UPDATE hoteis SET nome = %s WHERE rid = %s", (nome, rid))
                elif tipo == 'DELETE':
                    cur.execute("DELETE FROM hoteis WHERE rid = %s", (rid,))
                cur.execute("UPDATE solicitacoes_hoteis SET status = 'APPROVED' WHERE id = %s", (sid,))
            else:
                cur.execute("UPDATE solicitacoes_hoteis SET status = 'REJECTED' WHERE id = %s", (sid,))
    executar_backup_automatico()


# ─────────────────────────────────────────────────────────────────────────────
# USUÁRIOS — CRUD SEGURO
# ─────────────────────────────────────────────────────────────────────────────
def verify_login(username: str, password: str) -> dict | None:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password, nome_completo, is_admin, must_change_password, valor_base, perfil "
            "FROM usuarios WHERE username = %s",
            (username,)
        )
        row = cur.fetchone()
    if row and _check_pw(password, row[2]):
        return {
            "id":          row[0],
            "username":    row[1],
            "nome":        row[3],
            "admin":       bool(row[4]),
            "must_change": bool(row[5]),
            "valor_base":  _decrypt(row[6]),
            "perfil":      row[7] or "USER"
        }
    return None

def get_user_by_username(username: str) -> dict | None:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password, nome_completo, is_admin, must_change_password, valor_base, perfil "
            "FROM usuarios WHERE username = %s",
            (username,)
        )
        row = cur.fetchone()
    if row:
        return {
            "id":          row[0],
            "username":    row[1],
            "nome":        row[3],
            "admin":       bool(row[4]),
            "must_change": bool(row[5]),
            "valor_base":  _decrypt(row[6]),
            "perfil":      row[7] or "USER"
        }
    return None

def get_all_users() -> list[tuple]:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, nome_completo, is_admin, must_change_password, valor_base, perfil "
            "FROM usuarios ORDER BY LOWER(nome_completo)"
        )
        rows = cur.fetchall()
    # Decrypt salary in memory for listing
    return [(r[0], r[1], r[2], r[3], r[4], _decrypt(r[5]), r[6]) for r in rows]

def create_user(username: str, password: str, nome: str, perfil: str, valor_base: float = 0.0) -> bool:
    try:
        is_admin = True if perfil == 'ADMIN' else False
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (username, password, nome_completo, is_admin, perfil, must_change_password, valor_base) "
                "VALUES (%s, %s, %s, %s, %s, TRUE, %s)",
                (username, _hash_pw(password), nome, is_admin, perfil, _encrypt(valor_base))
            )
        return True
    except:
        return False

def update_user(uid: int, username: str, nome: str, perfil: str, valor_base: float, password: str | None = None) -> bool:
    try:
        is_admin = True if perfil == 'ADMIN' else False
        with get_db() as conn:
            cur = conn.cursor()
            if password:
                cur.execute(
                    "UPDATE usuarios SET username=%s, nome_completo=%s, is_admin=%s, perfil=%s, "
                    "password=%s, must_change_password=TRUE, valor_base=%s WHERE id=%s",
                    (username, nome, is_admin, perfil, _hash_pw(password), _encrypt(valor_base), uid)
                )
            else:
                cur.execute(
                    "UPDATE usuarios SET username=%s, nome_completo=%s, is_admin=%s, perfil=%s, valor_base=%s WHERE id=%s",
                    (username, nome, is_admin, perfil, _encrypt(valor_base), uid)
                )
        return True
    except:
        return False

def update_password(uid: int, new_password: str):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET password=%s, must_change_password=FALSE WHERE id=%s", (_hash_pw(new_password), uid))

def reset_password_admin(uid: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET password=%s, must_change_password=TRUE WHERE id=%s", (_hash_pw("mudar123"), uid))

def delete_user(uid: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (uid,))


# ─────────────────────────────────────────────────────────────────────────────
# CHAMADOS — CRUD
# ─────────────────────────────────────────────────────────────────────────────
def save_chamado(data, caso, rid, hotel, inicio, termino, obs, motivo, username: str, vbase_snapshot: float = 0.0):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes, motivo, username, valor_base_snapshot) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data, caso or "", rid, hotel, inicio, termino, obs or None, motivo, username, _encrypt(vbase_snapshot))
        )
    executar_backup_automatico()

def get_all_chamados(username_filter: str | None = None, perfil: str | None = None, logged_username: str | None = None) -> list[tuple]:
    with get_db() as conn:
        cur = conn.cursor()
        
        # Trava de Segurança: Se for USER, ignora o filtro externo e usa o username logado
        if perfil == 'USER' and logged_username:
            final_username = logged_username
        else:
            final_username = username_filter

        if final_username:
            cur.execute(
                "SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot, username "
                "FROM chamados WHERE username = %s ORDER BY data ASC, inicio ASC",
                (final_username,)
            )
        else:
            cur.execute(
                "SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot, username "
                "FROM chamados ORDER BY data ASC, inicio ASC"
            )
        rows = cur.fetchall()

    res = []
    for r in rows:
        vbs = 0.0
        if len(r) > 9 and r[9]:
            vbs = _decrypt(r[9])
        # Converter data DATE do PostgreSQL para string 'YYYY-MM-DD' para compatibilidade
        data_str = r[1].strftime("%Y-%m-%d") if hasattr(r[1], 'strftime') else str(r[1])
        res.append((r[0], data_str, r[2], r[3], r[4], r[5], r[6], r[7], r[8], vbs, r[10]))
    return res

def get_chamado_by_id(cid: int) -> tuple | None:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot, username "
            "FROM chamados WHERE id = %s",
            (cid,)
        )
        row = cur.fetchone()
    if row:
        vbs = 0.0
        if len(row) > 9 and row[9]:
            vbs = _decrypt(row[9])
        # Converter data DATE do PostgreSQL para string 'YYYY-MM-DD' para compatibilidade
        data_str = row[1].strftime("%Y-%m-%d") if hasattr(row[1], 'strftime') else str(row[1])
        return (row[0], data_str, row[2], row[3], row[4], row[5], row[6], row[7], row[8], vbs, row[10])
    return None

def update_chamado(cid, data, caso, rid, hotel, inicio, termino, obs, motivo):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE chamados SET data=%s, caso=%s, pms=%s, hotel=%s, inicio=%s, termino=%s, observacoes=%s, motivo=%s WHERE id=%s",
            (data, caso or "", rid, hotel, inicio, termino, obs or None, motivo, cid)
        )
    executar_backup_automatico()

def delete_chamado(cid: int):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM chamados WHERE id = %s", (cid,))
    executar_backup_automatico()

def delete_chamados_bulk(cids: list[int]):
    if not cids:
        return
    with get_db() as conn:
        cur = conn.cursor()
        # Usar IN com tupla para deletar em lote de forma eficiente
        cur.execute("DELETE FROM chamados WHERE id = ANY(%s)", (cids,))
    executar_backup_automatico()


if __name__ == "__main__":
    init_db()
    print("DB PostgreSQL inicializado com sucesso (.env ativo).")
