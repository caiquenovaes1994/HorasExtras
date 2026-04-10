import sqlite3
import os
import hashlib
import shutil

# Nova localização do banco de dados
DB_DIR = "data"
DB_NAME = os.path.join(DB_DIR, "horas_extras.db")
EXTERNAL_SOURCE = os.path.join(DB_DIR, "hotels_source.sqlite")

def get_connection():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Chamados (INC agora opcional na lógica, mas campo mantido)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            caso TEXT,
            pms TEXT,
            hotel TEXT,
            inicio TIME NOT NULL,
            termino TIME NOT NULL,
            observacoes TEXT
        )
    """)
    
    # Usuários com flag must_change_password
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nome_completo TEXT,
            is_admin BOOLEAN DEFAULT 0,
            must_change_password BOOLEAN DEFAULT 1
        )
    """)
    
    # Hotéis com constraint UNIQUE no RID
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hoteis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rid TEXT UNIQUE,
            nome TEXT NOT NULL
        )
    """)
    
    # Admin Padrão
    admin_user = "cnovaes"
    admin_pw = hash_password("Luigi170513")
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (admin_user,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password)
            VALUES (?, ?, ?, 1, 0)
        """, (admin_user, admin_pw, "CAIQUE NOVAES"))
    
    # Hotel Obrigatório
    cursor.execute("SELECT id FROM hoteis WHERE rid = 'B669'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO hoteis (rid, nome) VALUES ('B669', 'Ibis Caruaru')")
    
    conn.commit()
    conn.close()
    sync_hotels()

def sync_hotels():
    """Sincroniza do arquivo fonte usando SELECT DISTINCT."""
    if os.path.exists(EXTERNAL_SOURCE):
        try:
            ext_conn = sqlite3.connect(EXTERNAL_SOURCE)
            ext_cursor = ext_conn.cursor()
            # Usar DISTINCT para evitar duplicados da fonte
            ext_cursor.execute("SELECT DISTINCT rid, nome FROM hotels WHERE rid IS NOT NULL")
            hotels_data = ext_cursor.fetchall()
            ext_conn.close()
            
            conn = get_connection()
            cursor = conn.cursor()
            for rid, nome in hotels_data:
                cursor.execute("INSERT OR IGNORE INTO hoteis (rid, nome) VALUES (?, ?)", (rid, nome))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro na sincronização: {e}")

# --- CRUD Hotéis ---
def get_hoteis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rid, nome FROM hoteis ORDER BY nome ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_hotel(rid, nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO hoteis (rid, nome) VALUES (?, ?)", (rid, nome))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def update_hotel(old_rid, new_rid, new_nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE hoteis SET rid = ?, nome = ? WHERE rid = ?", (new_rid, new_nome, old_rid))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def delete_hotel(rid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hoteis WHERE rid = ?", (rid,))
    conn.commit()
    conn.close()

# --- CRUD Usuários ---
def verify_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, nome_completo, is_admin, must_change_password FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user[2] == hash_password(password):
        return {"id": user[0], "username": user[1], "nome": user[3], "admin": user[4], "must_change": user[5]}
    return None

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, nome_completo, is_admin, must_change_password FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, password, nome, is_admin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, nome_completo, is_admin, must_change_password) VALUES (?, ?, ?, ?, 1)", 
                       (username, hash_password(password), nome, 1 if is_admin else 0))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def update_user(uid, username, nome, is_admin, password=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if password:
            cursor.execute("UPDATE usuarios SET username=?, nome_completo=?, is_admin=?, password=?, must_change_password=1 WHERE id=?", 
                           (username, nome, 1 if is_admin else 0, hash_password(password), uid))
        else:
            cursor.execute("UPDATE usuarios SET username=?, nome_completo=?, is_admin=? WHERE id=?", 
                           (username, nome, 1 if is_admin else 0, uid))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def delete_user(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
    conn.commit()
    conn.close()

def update_password(uid, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET password = ?, must_change_password = 0 WHERE id = ?",
        (hash_password(new_password), uid)
    )
    conn.commit()
    conn.close()

def set_password_changed(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET must_change_password = 0 WHERE id = ?", (uid,))
    conn.commit()
    conn.close()

# --- Chamados ---
def save_chamado(data, caso, pms, hotel, inicio, termino, obs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes) VALUES (?,?,?,?,?,?,?)", 
                   (data, caso, pms, hotel, inicio, termino, obs))
    conn.commit()
    conn.close()

def get_all_chamados():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chamados ORDER BY data DESC, inicio ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_chamado(cid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chamados WHERE id = ?", (cid,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
