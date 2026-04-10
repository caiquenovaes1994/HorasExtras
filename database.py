import sqlite3
import os
import hashlib
import shutil

DB_NAME = "horas_extras.db"
EXTERNAL_DB_PATH = r"C:\Users\caiqu\.gemini\antigravity\scratch\SNOW_INC\server\database.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de Chamados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            caso TEXT NOT NULL,
            pms TEXT,
            hotel TEXT,
            inicio TIME NOT NULL,
            termino TIME NOT NULL,
            observacoes TEXT
        )
    """)
    
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nome_completo TEXT,
            is_admin BOOLEAN DEFAULT 0,
            precisa_trocar_senha BOOLEAN DEFAULT 1
        )
    """)
    
    # Tabela de Hotéis (Cache local)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hoteis (
            id INTEGER PRIMARY KEY,
            rid TEXT,
            nome TEXT
        )
    """)
    
    # Criar Admin Padrão
    admin_username = "cnovaes"
    admin_password = hash_password("Luigi170513")
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (admin_username,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (username, password, nome_completo, is_admin, precisa_trocar_senha)
            VALUES (?, ?, ?, ?, ?)
        """, (admin_username, admin_password, "CAIQUE NOVAES", 1, 0))
    
    conn.commit()
    conn.close()
    
    # Sincronizar Hotéis
    sync_hotels()

def sync_hotels():
    if os.path.exists(EXTERNAL_DB_PATH):
        try:
            # Conectar ao banco externo
            ext_conn = sqlite3.connect(EXTERNAL_DB_PATH)
            ext_cursor = ext_conn.cursor()
            ext_cursor.execute("SELECT rid, nome FROM hotels")
            hotels_data = ext_cursor.fetchall()
            ext_conn.close()
            
            # Atualizar cache local
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hoteis")
            cursor.executemany("INSERT INTO hoteis (rid, nome) VALUES (?, ?)", hotels_data)
            conn.commit()
            conn.close()
            print("Lista de hotéis sincronizada com sucesso.")
        except Exception as e:
            print(f"Erro ao sincronizar hotéis: {e}")
    else:
        print(f"Aviso: Banco de dados externo não encontrado em {EXTERNAL_DB_PATH}")

def get_hoteis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rid, nome FROM hoteis ORDER BY nome ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Funções de Usuário
def verify_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, nome_completo, is_admin, precisa_trocar_senha FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        return {
            "id": user[0],
            "username": user[1],
            "nome_completo": user[3],
            "is_admin": user[4],
            "precisa_trocar_senha": user[5]
        }
    return None

def update_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET password = ?, precisa_trocar_senha = 0 WHERE id = ?", (hash_password(new_password), user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, nome_completo, is_admin, precisa_trocar_senha FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, password, nome_completo, is_admin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (username, password, nome_completo, is_admin, precisa_trocar_senha)
            VALUES (?, ?, ?, ?, 1)
        """, (username, hash_password(password), nome_completo, 1 if is_admin else 0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Funções de Chamados
def save_chamado(data, caso, pms, hotel, inicio, termino, observacoes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chamados (data, caso, pms, hotel, inicio, termino, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data, caso, pms, hotel, inicio, termino, observacoes))
    conn.commit()
    conn.close()

def get_all_chamados():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chamados ORDER BY data DESC, inicio ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_chamado(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chamados WHERE id = ?", (id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
