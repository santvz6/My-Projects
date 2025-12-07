import sqlite3

def create_db():
    conn = sqlite3.connect('db/session.db')  # Esto creará un nuevo archivo de base de datos 'session.db'
    c = conn.cursor()
    # Crear una nueva tabla
    c.execute('''CREATE TABLE IF NOT EXISTS session_data (username TEXT)''')
    conn.commit()
    conn.close()


def save_session(username):
    conn = sqlite3.connect('db/session.db')
    c = conn.cursor()
    # Insertar los datos de la sesión
    c.execute("INSERT INTO session_data (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_session():
    conn = sqlite3.connect('db/session.db')
    c = conn.cursor()
    # Recuperar el último nombre de usuario insertado
    c.execute("SELECT username FROM session_data ORDER BY ROWID DESC LIMIT 1")
    username = c.fetchone()
    conn.close()
    return username[0] if username else None
