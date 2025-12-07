import sqlite3
from config import score

def create_database():
    # Conectarse a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('db/users.db')
    
    # Crear una nueva tabla (solo si no existe)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  login TEXT PRIMARY KEY,
                  password TEXT NOT NULL,
                  name TEXT,
                  surname TEXT,
                  score INTEGER
              )
              ''')
    
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def add_user(login, password, name, surname):
    # Conectarse a la base de datos
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    # Intentar insertar los datos del usuario en la base de datos
    try:
        c.execute('''
                  INSERT INTO users (login, password, name, surname, score)
                  VALUES (?, ?, ?, ?, ?)
                  ''', (login, password, name, surname, score))
        print("Usuario añadido con éxito.")
    except sqlite3.IntegrityError:
        # Esto ocurrirá si hay una violación de la restricción de unicidad (por ejemplo, el login ya existe)
        print(f"El login '{login}' ya existe.")
    
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def check_credentials(login, password):
    """Comprueba si el nombre de usuario y la contraseña existen en la base de datos."""
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    user = c.fetchone()
    
    conn.close()
    
    return user is not None

def check_login_exist(login):
    """Comprueba si el nombre de usuario existe en la base de datos."""
    with sqlite3.connect('db/users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = c.fetchone()
    
    return user is not None

def get_user_name(login):
    # Conectarse a la base de datos
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    try:
        # Suponiendo que 'c' es un objeto cursor para tu base de datos
        c.execute("SELECT name, surname FROM users WHERE login = ?", (login,))
        result = c.fetchall()
        for row in result:
            print(row)
            return row
    except sqlite3.IntegrityError:
        # Esto ocurrirá si hay una violación de la restricción de unicidad (por ejemplo, el login ya existe)
        print(f"Usuario no existe")
