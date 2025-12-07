from PyQt5 import QtWidgets, QtCore 
from ui_files.signup_window import Ui_MainWindow as Ui_SignupWindow
import styles
from db.db_logic import *

class SignupWindow(QtWidgets.QMainWindow):
    successful_signup = QtCore.pyqtSignal()
    back_login = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # Crea una instancia de la interfaz de usuario de la ventana de inicio de sesión
        self.ui = Ui_SignupWindow()
        self.ui.setupUi(self)

        # Conectar el botón de inicio de sesión al método de inicio de sesión
        self.ui.pushButton_crearCuenta.clicked.connect(self.crear_cuenta)

        # Conectar el botón de volver al inicio de sesión al método correspondiente
        self.ui.pushButton_back_toLogin.clicked.connect(self.backToLogin)

        # Establecer el tamaño fijo para la ventana
        self.setFixedSize(self.size())
    
    def backToLogin(self):
        self.back_login.emit()

    def crear_cuenta(self):
        self.ui.label_warnings.setText("")
        # Recuperar los valores ingresados
        nombre = self.ui.lineEdit_nombre.text()
        apellidos = self.ui.lineEdit_apellidos.text()
        login = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()

        # Lista de todas las ediciones de línea para un procesamiento más fácil
        line_edits = [
            self.ui.lineEdit_nombre,
            self.ui.lineEdit_apellidos,
            self.ui.lineEdit_login,
            self.ui.lineEdit_password
        ]

        # Suponer inicialmente que todos los valores son correctos
        all_correct = True

        # Verificar cada entrada y actualizar su estilo en consecuencia
        for le in line_edits:
            if not le.text():
                le.setStyleSheet(styles.lineEdit_incorrectInputStyle)
                all_correct = False
            else:
                le.setStyleSheet(styles.lineEdit_correctInputStyle)

        # Verificación adicional para la longitud de la contraseña
        if len(password) < 6:
            self.ui.lineEdit_password.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            self.ui.label_warnings.setText("Contraseña debe tener como mínimo 6 símbolos")
            all_correct = False

        # Verificar si el nombre de usuario ya existe
        if check_login_exist(login):
            self.ui.lineEdit_login.setStyleSheet(styles.lineEdit_incorrectInputStyle)
            self.ui.label_warnings.setText("Nombre de usuario ya existe")
            all_correct = False

        # Si todos los valores son correctos, emitir la señal
        if all_correct:
            self.successful_signup.emit()
            add_user(login, password, nombre, apellidos)

    def hideWindow(self):
        # Minimizar la ventana
        self.showMinimized()

    def close(self):
        self.hide()

    def open(self):
        # Mostrar la ventana principal
        self.show()
        self.ui.label_warnings.setText("")
        self.ui.lineEdit_nombre.setText("")
        self.ui.lineEdit_apellidos.setText("")
        self.ui.lineEdit_login.setText("")
        self.ui.lineEdit_password.setText("")
        # Lista de todas las ediciones de línea para un procesamiento más fácil
        line_edits = [
            self.ui.lineEdit_nombre,
            self.ui.lineEdit_apellidos,
            self.ui.lineEdit_login,
            self.ui.lineEdit_password
        ]

        for le in line_edits:
            le.setStyleSheet(styles.lineEdit_correctInputStyle)
