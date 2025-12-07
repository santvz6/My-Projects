from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import QFileDialog
from ui_files.main_window import Ui_MainWindow
import db.db_logic as db_logic
from db.session import get_session


def setup(self):
    setup_buttons(self)
    # setup_lineEdit(self)

def setup_buttons(self):
    pass

def setup_lineEdit(self):
    login = get_session()
    user, apellidos = db_logic.get_user_name(login)
    self.ui.label_4.setText(str(user)) # Linea con nombre del usario

    self.ui.label_7.setText(str(apellidos)) # Linea con apellidos del usario