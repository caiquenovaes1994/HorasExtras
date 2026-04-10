import sqlite3
import os
import hashlib

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
DB_DIR  = "data"
DB_NAME = os.path.join(DB_DIR, "horas_extras.db")
EXTERNAL_SOURCE = os.path.join(DB_DIR, "hotels_source.sqlite")


def get_connection() -> sqlite3.Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_NAME, check_same_thread=False, timeout=10)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
def init_db():
    conn   = get_connection()
    cursor = conn.cursor()

    # WAL mode: permite leituras concorrentes sem bloquear (essencial com Streamlit)
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
            observacoes TEXT
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            username             TEXT UNIQUE NOT NULL,
            password             TEXT NOT NULL,
            nome_completo        TEXT,
            is_admin             BOOLEAN DEFAULT 0,
            must_change_password BOOLEAN DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS hoteis (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            rid  TEXT UNIQUE,
            nome TEXT NOT NULL
        );
    """)

    # Admin padrão
    cursor.execute("SELECT id FROM usuarios WHERE username = 'cnovaes'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password) "
            "VALUES ('cnovaes', ?, 'CAIQUE NOVAES', 1, 0)",
            (_hash("Luigi170513"),)
        )

    # Hotel obrigatório
    cursor.execute("INSERT OR IGNORE INTO hoteis (rid, nome) VALUES ('B669', 'Ibis Caruaru')")

    conn.commit()
    conn.close()

    # Sincroniza hotéis externos apenas se a tabela estiver praticamente vazia
    conn2   = get_connection()
    cur2    = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM hoteis")
    total   = cur2.fetchone()[0]
    conn2.close()
    if total <= 1:
        _sync_hotels()


def _sync_hotels():
    """Importa hotéis do SQLite externo (somente uma vez, quando vazio)."""
    if not os.path.exists(EXTERNAL_SOURCE):
        return
    try:
        ext = sqlite3.connect(EXTERNAL_SOURCE)
        rows = ext.execute(
            "SELECT DISTINCT rid, nome FROM hotels WHERE rid IS NOT NULL AND rid != ''"
        ).fetchall()
        ext.close()

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO hoteis (rid, nome) VALUES (?, ?)", rows)
        conn.commit()
        conn.close()
        print(f"[sync] {len(rows)} hotéis importados.")
    except Exception as e:
        print(f"[sync] Erro: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# HOTÉIS — CRUD
# ─────────────────────────────────────────────────────────────────────────────
def get_hoteis() -> list[tuple]:
    """Retorna lista de (rid, nome) sem duplicatas, ordenada por nome."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT rid, nome FROM hoteis "
        "WHERE rid IS NOT NULL AND rid != '' "
        "GROUP BY rid "
        "ORDER BY nome COLLATE NOCASE ASC"
    ).fetchall()
    conn.close()
    return rows


def save_hotel(rid: str, nome: str) -> bool:
    try:
        conn = get_connection()
        conn.execute("INSERT INTO hoteis (rid, nome) VALUES (?, ?)", (rid, nome))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def update_hotel(old_rid: str, new_rid: str, new_nome: str) -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE hoteis SET rid = ?, nome = ? WHERE rid = ?",
            (new_rid, new_nome, old_rid)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def delete_hotel(rid: str):
    conn = get_connection()
    conn.execute("DELETE FROM hoteis WHERE rid = ?", (rid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# USUÁRIOS — CRUD
# ─────────────────────────────────────────────────────────────────────────────
def verify_login(username: str, password: str) -> dict | None:
    conn = get_connection()
    row  = conn.execute(
        "SELECT id, username, password, nome_completo, is_admin, must_change_password "
        "FROM usuarios WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    if row and row[2] == _hash(password):
        return {
            "id":          row[0],
            "username":    row[1],
            "nome":        row[3],
            "admin":       bool(row[4]),
            "must_change": bool(row[5]),
        }
    return None


def get_all_users() -> list[tuple]:
    conn  = get_connection()
    rows  = conn.execute(
        "SELECT id, username, nome_completo, is_admin, must_change_password FROM usuarios ORDER BY nome_completo"
    ).fetchall()
    conn.close()
    return rows


def create_user(username: str, password: str, nome: str, is_admin: bool) -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password) "
            "VALUES (?, ?, ?, ?, 1)",
            (username, _hash(password), nome, 1 if is_admin else 0)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def update_user(uid: int, username: str, nome: str, is_admin: bool, password: str | None = None) -> bool:
    try:
        conn = get_connection()
        if password:
            conn.execute(
                "UPDATE usuarios SET username=?, nome_completo=?, is_admin=?, password=?, must_change_password=1 WHERE id=?",
                (username, nome, 1 if is_admin else 0, _hash(password), uid)
            )
        else:
            conn.execute(
                "UPDATE usuarios SET username=?, nome_completo=?, is_admin=? WHERE id=?",
                (username, nome, 1 if is_admin else 0, uid)
            )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def update_password(uid: int, new_password: str):
    conn = get_connection()
    conn.execute(
        "UPDATE usuarios SET password=?, must_change_password=0 WHERE id=?",
        (_hash(new_password), uid)
    )
    conn.commit()
    conn.close()


def delete_user(uid: int):
    conn = get_connection()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# CHAMADOS — CRUD
# ─────────────────────────────────────────────────────────────────────────────
def save_chamado(data, caso, pms, hotel, inicio, termino, obs):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        # Usa string vazia ao invés de None para compatibilidade com schema antigo (NOT NULL)
        (data, caso or "", pms, hotel, inicio, termino, obs or None)
    )
    conn.commit()
    conn.close()


def get_all_chamados() -> list[tuple]:
    conn  = get_connection()
    rows  = conn.execute(
        "SELECT * FROM chamados ORDER BY data ASC, inicio ASC"
    ).fetchall()
    conn.close()
    return rows


def get_chamado_by_id(cid: int) -> tuple | None:
    conn = get_connection()
    row  = conn.execute("SELECT * FROM chamados WHERE id = ?", (cid,)).fetchone()
    conn.close()
    return row


def update_chamado(cid, data, caso, pms, hotel, inicio, termino, obs):
    conn = get_connection()
    conn.execute(
        "UPDATE chamados SET data=?, caso=?, pms=?, hotel=?, inicio=?, termino=?, observacoes=? WHERE id=?",
        (data, caso or "", pms, hotel, inicio, termino, obs or None, cid)
    )
    conn.commit()
    conn.close()


def delete_chamado(cid: int):
    conn = get_connection()
    conn.execute("DELETE FROM chamados WHERE id = ?", (cid,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("DB inicializado.")
