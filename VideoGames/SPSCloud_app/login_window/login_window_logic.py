from PyQt5 import QtWidgets, QtCore 
from ui_files.login_window import Ui_MainWindow as Ui_LoginWindow
import main_window.main_window_setup
import styles
import sqlite3
from db.db_logic import *
import db.session as session

class LoginWindow(QtWidgets.QMainWindow):
    successful_login = QtCore.pyqtSignal()  # Señal para el inicio de sesión exitoso
    start_signup = QtCore.pyqtSignal()  # Señal para empezar el proceso de registro

    def __init__(self):
        super().__init__()

        self.ui = Ui_LoginWindow()  # Crea una instancia de la UI para la ventana de inicio de sesión
        self.ui.setupUi(self)  # Inicializa la UI

        # Conecta los botones a sus respectivos métodos
        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_signup.clicked.connect(self.signup_clicked)

        self.setFixedSize(self.size())  # Establece un tamaño fijo para la ventana
        self.set_styles()  # Aplica estilos iniciales

    def signup_clicked(self):
        # Emite la señal para iniciar el proceso de registro
        self.start_signup.emit()

    def login(self):
        # Recoge el nombre de usuario y contraseña del formulario
        username = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()

        # Verifica las credenciales
        if check_credentials(username, password):
            print("Inicio de sesión exitoso")
            # Aplica estilo de input correcto
            self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_correctInputStyle)
            self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_correctInputStyle)
            
            session.create_db()  # Crea/verifica la base de datos
            session.save_session(username)  # Guarda la sesión del usuario

            self.successful_login.emit()  # Emite la señal de inicio de sesión exitoso

        else:
            print("Inicio de sesión fallido")
            # Aplica estilo de input incorrecto
            self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_incorrectInputStyle)

            # Verifica si el nombre de usuario existe en la base de datos
            conn = sqlite3.connect('db/users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login = ?", (username,))
            user_with_login = c.fetchone()
            conn.close()

            # Actualiza la interfaz según si el nombre de usuario o la contraseña son incorrectos
            if not user_with_login:
                print("Nombre de usuario incorrecto")
                self.ui.label_warnings.setText("Nombre de usuario incorrecto")
                self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            else:
                self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_correctInputStyle)
                print("Contraseña incorrecta")
                self.ui.label_warnings.setText("Contraseña incorrecta")
                self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_incorrectInputStyle)

    def hideWindow(self):
        # Minimiza la ventana
        self.showMinimized()

    def close(self):
        # Oculta la ventana
        self.hide()

    def open(self):
        # Muestra la ventana principal
        self.show()
        self.set_styles()  # Aplica estilos

    def set_styles(self):
        # Reinicia los estilos y los campos de texto
        self.ui.label_warnings.setText("")
        self.ui.lineEdit_login.setText("")
        self.ui.lineEdit_password.setText("")
        line_edits = [self.ui.lineEdit_login, self.ui.lineEdit_password]

        for le in line_edits:
            le.setStyleSheet(styles.lineEdit_correctInputStyle)
