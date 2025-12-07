from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import QFileDialog
import time
from datetime import datetime
from datetime import timedelta
import asyncio
import qasync
from ui_files.main_window import Ui_MainWindow
from main_window.main_window_setup import setup, setup_lineEdit

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Crea una instancia de la interfaz de usuario de la ventana principal
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        setup(self)

    def open(self):
        # Mostrar la ventana principal
        self.show()
        setup_lineEdit(self)


