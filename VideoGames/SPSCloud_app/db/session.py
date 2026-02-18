import sqlite3

def create_db():
    # Establece conexión con la base de datos SQLite, creándola si no existe
    conn = sqlite3.connect('db/session.db')
    c = conn.cursor()

    # Crea una tabla 'session_data' si no existe para almacenar los datos de la sesión
    c.execute('''CREATE TABLE IF NOT EXISTS session_data (username TEXT)''')

    # Guarda los cambios y cierra la conexión a la base de datos
    conn.commit()
    conn.close()

def save_session(username):
    # Conecta a la base de datos SQLite
    conn = sqlite3.connect('db/session.db')
    c = conn.cursor()

    # Inserta el nombre de usuario en la tabla 'session_data'
    c.execute("INSERT INTO session_data (username) VALUES (?)", (username,))

    # Guarda los cambios y cierra la conexión a la base de datos
    conn.commit()
    conn.close()

def get_session():
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('db/session.db')
        c = conn.cursor()

        # Recupera el último nombre de usuario guardado en 'session_data'
        c.execute("SELECT username FROM session_data ORDER BY ROWID DESC LIMIT 1")
        username = c.fetchone()

        # Cierra la conexión a la base de datos
        conn.close()

        # Devuelve el nombre de usuario si existe, de lo contrario devuelve None
        return username[0] if username else None
    except:
        # En caso de una excepción, no hace nada (podría ser útil manejar o registrar errores aquí)
        pass
