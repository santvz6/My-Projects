from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import QFileDialog
import time
from datetime import datetime
from datetime import timedelta
import asyncio
import qasync
from ui_files.main_window import Ui_MainWindow
from main_window.main_window_setup import setup, setup_profile_labels
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Crea una instancia de la interfaz de usuario de la ventana principal
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Conectar el QLabel 'label_autor1' con el método 'on_label_autor1_clicked'
        self.ui.label_autor1.mouseReleaseEvent = self.on_label_autor1_clicked

    def on_label_autor1_clicked(self, event):
        # Este método se llamará cuando se haga clic en 'label_autor1'
        # Solo reaccionar a los clics del botón izquierdo del ratón
        if event.button() == Qt.LeftButton:
            QDesktopServices.openUrl(QUrl("https://linktr.ee/stanislav_gatin"))

    def open(self):
        # Mostrar la ventana principal
        self.show()
        setup_profile_labels(self)
        setup(self)

