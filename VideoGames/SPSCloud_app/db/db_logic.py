import sqlite3
import sys
sys.path.insert(1, '../SPSCloud_app')
from config import score
import styles
import os
import db.session as session

def create_database():
    # Establece conexión con la base de datos SQLite, creándola si no existe
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()

    # Crea una tabla 'users' si no existe para almacenar los datos de los usuarios
    c.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  login TEXT PRIMARY KEY,
                  password TEXT NOT NULL,
                  name TEXT,
                  surname TEXT,
                  score INTEGER,
                  user_photo TEXT
              )
              ''')

    # Guarda los cambios y cierra la conexión a la base de datos
    conn.commit()
    conn.close()

def add_user(login, password, name, surname):
    # Conecta a la base de datos SQLite
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()

    # Intenta insertar los datos del usuario en la tabla 'users'
    try:
        c.execute('''
                  INSERT INTO users (login, password, name, surname, score, user_photo)
                  VALUES (?, ?, ?, ?, ?, ?)
                  ''', (login, password, name, surname, score, str('../SPSCloud_app/img/profile/1.png')))
        print("Usuario añadido con éxito.")
    except sqlite3.IntegrityError:
        # Se ejecuta si el 'login' ya existe en la base de datos
        print(f"El login '{login}' ya existe.")

    # Guarda los cambios y cierra la conexión a la base de datos
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
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE login = ?", (login,))
    user = c.fetchone()
    
    conn.close()
    
    return user is not None

def get_user_name(login):
    # Conecta a la base de datos SQLite y obtiene el nombre y apellido del usuario
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT name, surname FROM users WHERE login = ?", (login,))
    result = c.fetchall()

    conn.close()

    # Devuelve el nombre y apellido si el usuario existe
    for row in result:
        return row

def get_user_photo(login):
    # Conecta a la base de datos SQLite y obtiene la foto del usuario
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT user_photo FROM users WHERE login = ?", (login,))
    result = c.fetchall()

    conn.close()

    # Devuelve la ruta de la foto si el usuario existe
    for row in result:
        return row

def cambiar_contrasena(self):
    # Intenta obtener la nueva contraseña y el nombre de usuario de la sesión actual
    nueva_contrasena = self.ui.lineEdit_cambiar_contrasena.text()
    login = session.get_session()

    # Verifica la longitud de la nueva contraseña
    if len(nueva_contrasena) < 6:
        # Actualiza la interfaz de usuario para reflejar un error
        self.ui.lineEdit_cambiar_contrasena.setStyleSheet(styles.lineEdit_incorrectInputStyle)
        self.ui.label_cambiar_contrasena_warning.setText("La contraseña debe tener como mínimo 6 símbolos")
    else:
        # Conecta a la base de datos SQLite y actualiza la contraseña del usuario
        conn = sqlite3.connect('db/users.db')
        c = conn.cursor()

        try:
            c.execute("UPDATE users SET password = ? WHERE login = ?", (nueva_contrasena, login))
            conn.commit()
            # Actualiza la interfaz de usuario para reflejar el éxito
            self.ui.lineEdit_cambiar_contrasena.setStyleSheet(styles.lineEdit_correctInputStyle)
            self.ui.label_cambiar_contrasena_warning.setText("Contraseña actualizada con éxito.")
        except sqlite3.Error as e:
            # Manejo de errores en caso de falla
            print(f"Error al actualizar contraseña: {e}")
            self.ui.label_cambiar_contrasena_warning.setText("Error al actualizar contraseña.")
        finally:
            conn.close()

def cambiar_foto(self):
    # Intenta obtener el nuevo camino de la foto y el nombre de usuario de la sesión actual
    path = self.ui.lineEdit_cambiar_foto.text()
    login = session.get_session()

    # Verifica si el archivo de la foto existe
    if not os.path.exists(path):
        # Actualiza la interfaz de usuario para reflejar un error
        self.ui.lineEdit_cambiar_foto.setStyleSheet(styles.lineEdit_incorrectInputStyle)
        self.ui.label_cambiar_foto_warning.setText("El archivo no existe.")
    else:
        # Conecta a la base de datos SQLite y actualiza la foto del perfil del usuario
        conn = sqlite3.connect('db/users.db')
        c = conn.cursor()

        try:
            c.execute("UPDATE users SET user_photo = ? WHERE login = ?", (path, login))
            conn.commit()
            # Actualiza la interfaz de usuario para reflejar el éxito
            self.ui.lineEdit_cambiar_foto.setStyleSheet(styles.lineEdit_correctInputStyle)
            self.ui.label_cambiar_foto_warning.setText("Foto de perfil actualizada con éxito.")
        except sqlite3.Error as e:
            # Manejo de errores en caso de falla
            print(f"Error al actualizar la foto de perfil: {e}")
            self.ui.label_cambiar_foto_warning.setText("Error al actualizar la foto de perfil.")
        finally:
            conn.close()

def get_user_score():
    # Obtiene el puntaje del usuario actual de la base de datos
    login = session.get_session()
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT score FROM users WHERE login = ?", (login,))
    score = c.fetchone()

    conn.close()

    # Devuelve el puntaje si el usuario existe
    return int(score[0]) if score else None

def update_user_score(new_score):
    # Actualiza el puntaje del usuario actual en la base de datos
    login = session.get_session()
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    try:
        c.execute("UPDATE users SET score = ? WHERE login = ?", (new_score, login))
        conn.commit()
        print("Puntaje actualizado con éxito.")
    except sqlite3.Error as e:
        # Manejo de errores en caso de falla
        print(f"Error al actualizar el puntaje: {e}")
    finally:
        conn.close()

def print_user_info():
    # Imprime la información del usuario actual desde la base de datos
    login = session.get_session()
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE login = ?", (login,))
    user_info = c.fetchone()

    conn.close()

    # Imprime la información del usuario si existe
    if user_info:
        print(f"Información del Usuario '{login}':")
        # Considerar ocultar la contraseña por motivos de seguridad
        print(f"Login: {user_info[0]}, Contraseña: {user_info[1]}, Nombre: {user_info[2]}, Apellido: {user_info[3]}, Puntaje: {user_info[4]}, Foto de Usuario: {user_info[5]}")
    else:
        print("Usuario no encontrado.")
