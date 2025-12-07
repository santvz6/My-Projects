import sys
from PyQt5 import QtCore, QtWidgets
from login_window.login_window_logic import LoginWindow
from main_window.main_window_logic import MainWindow
from signup_window.signup_window_logic import SignupWindow
from db.db_logic import *
import qasync, asyncio

if __name__ == "__main__":
    # Crear la base de datos si no existe
    create_database()

    # Crear la instancia de QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Crear la instancia de LoginWindow
    login_window = LoginWindow() 

    # Configurar el bucle de eventos qasync para integración con asyncio
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Crear la instancia de MainWindow
    main_window = MainWindow()

    # Crear la instancia de SignupWindow
    signup_window = SignupWindow()

    # Conectar la señal successful_login de login_window al método open de main_window
    login_window.successful_login.connect(login_window.close)
    login_window.successful_login.connect(main_window.open)

    # Conectar la señal start_signup de login_window al método open de signup_window
    login_window.start_signup.connect(login_window.close)
    login_window.start_signup.connect(signup_window.open)

    # Conectar la señal successful_signup de signup_window al método open de login_window
    signup_window.successful_signup.connect(signup_window.close)
    signup_window.successful_signup.connect(login_window.open)

    # Conectar la señal back_login de signup_window al método open de login_window
    signup_window.back_login.connect(signup_window.close)
    signup_window.back_login.connect(login_window.open)

    # Mostrar la ventana de inicio de sesión
    login_window.show()

    # Ejecutar el bucle de eventos
    with loop:
        sys.exit(loop.run_forever())
