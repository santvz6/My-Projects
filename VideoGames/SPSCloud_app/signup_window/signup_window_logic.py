from PyQt5 import QtWidgets, QtCore 
from ui_files.signup_window import Ui_MainWindow as Ui_SignupWindow
import styles
from db.db_logic import *

class SignupWindow(QtWidgets.QMainWindow):
    successful_signup = QtCore.pyqtSignal()  # Señal emitida cuando el registro es exitoso
    back_login = QtCore.pyqtSignal()  # Señal para volver a la pantalla de inicio de sesión

    def __init__(self):
        super().__init__()

        self.ui = Ui_SignupWindow()  # Crea una instancia de la interfaz de usuario
        self.ui.setupUi(self)  # Inicializa la interfaz de usuario

        # Conectar botones a sus respectivos métodos
        self.ui.pushButton_crearCuenta.clicked.connect(self.crear_cuenta)
        self.ui.pushButton_back_toLogin.clicked.connect(self.backToLogin)

        self.setFixedSize(self.size())  # Establece un tamaño fijo para la ventana

        self.set_styles()  # Aplica estilos a los componentes de la interfaz
    
    def backToLogin(self):
        self.back_login.emit()  # Emite la señal para volver al inicio de sesión

    def crear_cuenta(self):
        self.ui.label_warnings.setText("")  # Limpia cualquier advertencia previa

        # Recuperar los valores ingresados por el usuario
        nombre = self.ui.lineEdit_nombre.text()
        apellidos = self.ui.lineEdit_apellidos.text()
        login = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()

        line_edits = [
            self.ui.lineEdit_nombre,
            self.ui.lineEdit_apellidos,
            self.ui.lineEdit_login,
            self.ui.lineEdit_password
        ]  # Lista de campos de texto para validación

        all_correct = True  # Indicador de que todos los campos son válidos

        # Verificar y actualizar estilos de cada campo de texto
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

        if all_correct:
            self.successful_signup.emit()  # Emite señal de registro exitoso
            add_user(login, password, nombre, apellidos)  # Añade el usuario a la base de datos

    def hideWindow(self):
        self.showMinimized()  # Minimiza la ventana

    def close(self):
        self.hide()  # Oculta la ventana

    def open(self):
        self.show()  # Muestra la ventana
        self.set_styles()  # Aplica estilos

    def set_styles(self):
        # Reinicia los estilos y campos de texto
        self.ui.label_warnings.setText("")
        self.ui.lineEdit_nombre.setText("")
        self.ui.lineEdit_apellidos.setText("")
        self.ui.lineEdit_login.setText("")
        self.ui.lineEdit_password.setText("")

        line_edits = [
            self.ui.lineEdit_nombre,
            self.ui.lineEdit_apellidos,
            self.ui.lineEdit_login,
            self.ui.lineEdit_password
        ]

        for le in line_edits:
            le.setStyleSheet(styles.lineEdit_correctInputStyle)
