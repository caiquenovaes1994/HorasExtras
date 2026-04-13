import sqlite3
import os
import bcrypt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO E SEGURANÇA
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

DB_DIR  = "data"
DB_NAME = os.path.join(DB_DIR, "horas_extras.db")
EXTERNAL_SOURCE = os.path.join(DB_DIR, "hotels_source.sqlite")

# Chave Secreta para Criptografia de Dados (Salários)
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_PWD  = os.getenv("ADMIN_PWD", "mudar123")

# Inicializa cifras apenas se a chave estiver presente
_cipher = Fernet(SECRET_KEY.encode()) if SECRET_KEY else None

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

def get_connection() -> sqlite3.Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_NAME, check_same_thread=False, timeout=10)


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZAÇÃO E MIGRAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
def init_db():
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS chamados (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data        DATE    NOT NULL,
            caso        TEXT,
            pms         TEXT,
            hotel       TEXT,
            inicio      TIME    NOT NULL,
            termino     TIME    NOT NULL,
            observacoes TEXT,
            motivo      TEXT
        );
        
        CREATE TABLE IF NOT EXISTS solicitacoes_hoteis (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            rid       TEXT NOT NULL,
            nome      TEXT NOT NULL,
            tipo      TEXT NOT NULL,
            user_id   INTEGER,
            status    TEXT DEFAULT 'PENDING'
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            username             TEXT UNIQUE NOT NULL,
            password             TEXT NOT NULL,
            nome_completo        TEXT,
            is_admin             BOOLEAN DEFAULT 0,
            must_change_password BOOLEAN DEFAULT 1,
            valor_base           TEXT DEFAULT '0.0'
        );

        CREATE TABLE IF NOT EXISTS hoteis (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            rid  TEXT UNIQUE,
            nome TEXT NOT NULL
        );
    """)

    # Migração para garantir que valor_base pode armazenar texto (tokens criptografados)
    try:
        # Verifica se o tipo da coluna precisa ser ajustado (SQLite é flexível, mas forçamos TEXT)
        cursor.execute("ALTER TABLE usuarios ADD COLUMN valor_base_secure TEXT DEFAULT '0.0'")
    except: pass

    # Admin padrão baseado no .env
    cursor.execute("SELECT id FROM usuarios WHERE username = 'cnovaes'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password) "
            "VALUES ('cnovaes', ?, 'CAIQUE NOVAES', 1, 0)",
            (_hash_pw(ADMIN_PWD),)
        )

    cursor.execute("INSERT OR IGNORE INTO hoteis (rid, nome) VALUES ('B669', 'Ibis Caruaru')")

    try:
        cursor.execute("ALTER TABLE chamados ADD COLUMN motivo TEXT")
    except: pass

    try:
        cursor.execute("ALTER TABLE chamados ADD COLUMN valor_base_snapshot TEXT DEFAULT '0.0'")
    except: pass

    conn.commit()
    conn.close()
    
    # Sincroniza hotéis externos
    conn2 = get_connection(); cur2 = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM hoteis"); total = cur2.fetchone()[0]
    conn2.close()
    if total <= 1: _sync_hotels()


def _sync_hotels():
    if not os.path.exists(EXTERNAL_SOURCE): return
    try:
        ext = sqlite3.connect(EXTERNAL_SOURCE)
        rows = ext.execute("SELECT DISTINCT rid, nome FROM hotels WHERE rid IS NOT NULL AND rid != ''").fetchall()
        ext.close()
        conn = get_connection(); cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO hoteis (rid, nome) VALUES (?, ?)", rows)
        conn.commit(); conn.close()
    except: pass


# ─────────────────────────────────────────────────────────────────────────────
# HOTÉIS E SOLICITAÇÕES
# ─────────────────────────────────────────────────────────────────────────────
def get_hoteis() -> list[tuple]:
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT rid, nome FROM hoteis WHERE rid IS NOT NULL AND rid != '' ORDER BY rid COLLATE NOCASE ASC").fetchall()
    conn.close()
    return rows

def criar_solicitacao_hotel(rid: str, nome: str, tipo: str, user_id: int):
    conn = get_connection()
    conn.execute("INSERT INTO solicitacoes_hoteis (rid, nome, tipo, user_id, status) VALUES (?, ?, ?, ?, 'PENDING')", (rid, nome, tipo, user_id))
    conn.commit(); conn.close()

def get_solicitacoes_pendentes() -> list[tuple]:
    conn = get_connection()
    rows = conn.execute("SELECT s.id, s.rid, s.nome, s.tipo, u.nome_completo FROM solicitacoes_hoteis s LEFT JOIN usuarios u ON s.user_id = u.id WHERE s.status = 'PENDING'").fetchall()
    conn.close()
    return rows

def processar_solicitacao(sid: int, aprovado: bool):
    conn = get_connection(); cursor = conn.cursor()
    row = cursor.execute("SELECT rid, nome, tipo FROM solicitacoes_hoteis WHERE id = ?", (sid,)).fetchone()
    if row:
        rid, nome, tipo = row
        if aprovado:
            if tipo == 'CREATE': cursor.execute("INSERT OR REPLACE INTO hoteis (rid, nome) VALUES (?, ?)", (rid, nome))
            elif tipo == 'EDIT': cursor.execute("UPDATE hoteis SET nome = ? WHERE rid = ?", (nome, rid))
            elif tipo == 'DELETE': cursor.execute("DELETE FROM hoteis WHERE rid = ?", (rid,))
            cursor.execute("UPDATE solicitacoes_hoteis SET status = 'APPROVED' WHERE id = ?", (sid,))
        else:
            cursor.execute("UPDATE solicitacoes_hoteis SET status = 'REJECTED' WHERE id = ?", (sid,))
    conn.commit(); conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# USUÁRIOS — CRUD SEGURO
# ─────────────────────────────────────────────────────────────────────────────
def verify_login(username: str, password: str) -> dict | None:
    conn = get_connection()
    row  = conn.execute("SELECT id, username, password, nome_completo, is_admin, must_change_password, valor_base FROM usuarios WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row and _check_pw(password, row[2]):
        return {
            "id":          row[0],
            "username":    row[1],
            "nome":        row[3],
            "admin":       bool(row[4]),
            "must_change": bool(row[5]),
            "valor_base":  _decrypt(row[6])
        }
    return None

def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    row  = conn.execute("SELECT id, username, password, nome_completo, is_admin, must_change_password, valor_base FROM usuarios WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return {
            "id":          row[0],
            "username":    row[1],
            "nome":        row[3],
            "admin":       bool(row[4]),
            "must_change": bool(row[5]),
            "valor_base":  _decrypt(row[6])
        }
    return None

def get_all_users() -> list[tuple]:
    conn  = get_connection()
    rows  = conn.execute("SELECT id, username, nome_completo, is_admin, must_change_password, valor_base FROM usuarios ORDER BY nome_completo COLLATE NOCASE").fetchall()
    conn.close()
    # Decrypt salary in memory for listing
    return [(r[0], r[1], r[2], r[3], r[4], _decrypt(r[5])) for r in rows]

def create_user(username: str, password: str, nome: str, is_admin: bool, valor_base: float = 0.0) -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password, valor_base) VALUES (?, ?, ?, ?, 1, ?)",
            (username, _hash_pw(password), nome, 1 if is_admin else 0, _encrypt(valor_base))
        )
        conn.commit(); conn.close()
        return True
    except: return False

def update_user(uid: int, username: str, nome: str, is_admin: bool, valor_base: float, password: str | None = None) -> bool:
    try:
        conn = get_connection()
        if password:
            conn.execute(
                "UPDATE usuarios SET username=?, nome_completo=?, is_admin=?, password=?, must_change_password=1, valor_base=? WHERE id=?",
                (username, nome, 1 if is_admin else 0, _hash_pw(password), _encrypt(valor_base), uid)
            )
        else:
            conn.execute("UPDATE usuarios SET username=?, nome_completo=?, is_admin=?, valor_base=? WHERE id=?", (username, nome, 1 if is_admin else 0, _encrypt(valor_base), uid))
        conn.commit(); conn.close()
        return True
    except: return False

def update_password(uid: int, new_password: str):
    conn = get_connection()
    conn.execute("UPDATE usuarios SET password=?, must_change_password=0 WHERE id=?", (_hash_pw(new_password), uid))
    conn.commit(); conn.close()

def reset_password_admin(uid: int):
    conn = get_connection()
    conn.execute("UPDATE usuarios SET password=?, must_change_password=1 WHERE id=?", (_hash_pw("mudar123"), uid))
    conn.commit(); conn.close()

def delete_user(uid: int):
    conn = get_connection()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
    conn.commit(); conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# CHAMADOS — CRUD
# ─────────────────────────────────────────────────────────────────────────────
def save_chamado(data, caso, rid, hotel, inicio, termino, obs, motivo, vbase_snapshot: float = 0.0):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data, caso or "", rid, hotel, inicio, termino, obs or None, motivo, _encrypt(vbase_snapshot))
    )
    conn.commit(); conn.close()

def get_all_chamados() -> list[tuple]:
    conn  = get_connection()
    rows  = conn.execute("SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot FROM chamados ORDER BY data ASC, inicio ASC").fetchall()
    conn.close()
    
    res = []
    for r in rows:
        vbs = 0.0
        if len(r) > 9 and r[9]:
            vbs = _decrypt(r[9])
        res.append((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], vbs))
    return res

def get_chamado_by_id(cid: int) -> tuple | None:
    conn = get_connection()
    row  = conn.execute("SELECT id, data, caso, pms, hotel, inicio, termino, observacoes, motivo, valor_base_snapshot FROM chamados WHERE id = ?", (cid,)).fetchone()
    conn.close()
    if row:
        vbs = 0.0
        if len(row) > 9 and row[9]:
            vbs = _decrypt(row[9])
        return (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], vbs)
    return None

def update_chamado(cid, data, caso, rid, hotel, inicio, termino, obs, motivo):
    conn = get_connection()
    conn.execute("UPDATE chamados SET data=?, caso=?, pms=?, hotel=?, inicio=?, termino=?, observacoes=?, motivo=? WHERE id=?", (data, caso or "", rid, hotel, inicio, termino, obs or None, motivo, cid))
    conn.commit(); conn.close()

def delete_chamado(cid: int):
    conn = get_connection()
    conn.execute("DELETE FROM chamados WHERE id = ?", (cid,))
    conn.commit(); conn.close()


if __name__ == "__main__":
    init_db()
    print("DB inicializado com sucesso (.env ativo).")
