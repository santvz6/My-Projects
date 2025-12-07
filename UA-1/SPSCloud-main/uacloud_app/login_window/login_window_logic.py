from PyQt5 import QtWidgets, QtCore 
from ui_files.login_window import Ui_MainWindow as Ui_LoginWindow
import main_window.main_window_setup
# from main_window_logic import MainWindow
import styles
import sqlite3
from db.db_logic import *
import db.session as session

class LoginWindow(QtWidgets.QMainWindow):
    # Define una señal para el inicio de sesión exitoso
    successful_login = QtCore.pyqtSignal()
    start_signup = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # Crea una instancia de la interfaz de usuario de la ventana de inicio de sesión
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # Conectar el botón de inicio de sesión al método de inicio de sesión
        self.ui.pushButton_login.clicked.connect(self.login)

        # Conectar el botón de registro al método de registro
        self.ui.pushButton_signup.clicked.connect(self.signup_clicked)

        # Establecer el tamaño fijo para la ventana
        self.setFixedSize(self.size())

    def signup_clicked(self):
        self.start_signup.emit()

    def login(self):
        # Obtener el nombre de usuario y la contraseña ingresados por el usuario
        username = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()

        # Realiza aquí tu lógica de inicio de sesión
        if check_credentials(username, password):
            print("Inicio de sesión exitoso")
            self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_correctInputStyle)
            self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_correctInputStyle)
            session.create_db()
            session.save_session(username)

            # Emitir la señal successful_login
            self.successful_login.emit()

        else:
            print("Inicio de sesión fallido")
            self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_incorrectInputStyle)

            # No deberíamos consultar la base de datos múltiples veces en una función.
            # Para mejorar la eficiencia, solo revisamos si el nombre de usuario existe (independientemente de la contraseña).
            conn = sqlite3.connect('db/users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login = ?", (username,))
            user_with_login = c.fetchone()
            conn.close()

            if not user_with_login:
                print("Nombre de usuario incorrecto")
                self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            else:
                self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_correctInputStyle)
                print("Contraseña incorrecta")
                self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_incorrectInputStyle)

    def hideWindow(self):
        # Minimizar la ventana
        self.showMinimized()

    def close(self):
        self.hide()

    def open(self):
        # Mostrar la ventana principal
        self.show()
