from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from ui_files.main_window import Ui_MainWindow
import db.db_logic as db_logic
from db.session import get_session
import styles
import config
import asyncio
import sys

def setup(self):
    # Configura los botones, la foto de perfil y los estilos de los campos de texto
    setup_buttons(self)
    setup_photo(self)
    setup_lineEdit_styles(self)

async def run_script_async(script_name):
    # Ejecuta un script de forma asíncrona
    process = await asyncio.create_subprocess_exec(
        sys.executable, script_name,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # Espera a que el script termine y recoge la salida
    stdout, stderr = await process.communicate()

    # Imprime la salida del script
    if stdout:
        print(f"[STDOUT]\n{stdout.decode()}")
    if stderr:
        print(f"[STDERR]\n{stderr.decode()}")


# Las siguientes funciones inician juegos específicos de forma asíncrona
def flappy_bird():
    sys.path.append('/Users/stanislavgatin/Documents/qt_apps/sps_cloud_app_versions/SPSCloud_app/juegos/flappy_bird')
    print(sys.path)
    asyncio.create_task(run_script_async('../SPSCloud_app/juegos/flappy_bird/SPSCloud.py'))

def kht():
    sys.path.append('/Users/stanislavgatin/Documents/qt_apps/sps_cloud_app_versions/SPSCloud_app/juegos/flappy_bird')
    print(sys.path)
    asyncio.create_task(run_script_async('../SPSCloud_app/juegos/flappy_bird/kht.py'))

def clicker():
    sys.path.append('/Users/stanislavgatin/Documents/qt_apps/sps_cloud_app_versions/SPSCloud_app/juegos/flappy_bird')
    print(sys.path)
    asyncio.create_task(run_script_async('../SPSCloud_app/juegos/flappy_bird/clicker.py'))

def dungeon():
    sys.path.append('/Users/stanislavgatin/Documents/qt_apps/sps_cloud_app_versions/SPSCloud_app/juegos/flappy_bird')
    print(sys.path)
    asyncio.create_task(run_script_async('../SPSCloud_app/juegos/flappy_bird/dungeon.py'))

def recargar_puntaje(self):
    # Actualiza el puntaje del usuario en la interfaz
    puntaje = db_logic.get_user_score()
    self.ui.label_3.setText(str(puntaje))

def chooseFile(self):
    # Abre un cuadro de diálogo para seleccionar una imagen
    fname, _ = QFileDialog.getOpenFileName(self, 'Seleccionar imagen', 
                                            QtCore.QDir.homePath(), 
                                            'Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)')
    if fname:
        self.ui.lineEdit_cambiar_foto.setText(fname)

def cambiar_foto(self):
    # Cambia la foto de perfil del usuario
    db_logic.cambiar_foto(self)
    setup_photo(self)

def setup_buttons(self):
    # Configura los botones para iniciar juegos y cambiar configuraciones del perfil
    self.ui.pushButton_10.clicked.connect(flappy_bird)
    self.ui.pushButton_8.clicked.connect(kht)
    self.ui.pushButton_11.clicked.connect(clicker)
    self.ui.pushButton_7.clicked.connect(dungeon)

    self.ui.pushButton_cambiar_contrasena.clicked.connect(lambda: db_logic.cambiar_contrasena(self))
    self.ui.pushButton_cambiar_foto.clicked.connect(lambda: cambiar_foto(self))
    self.ui.pushButton_select_image.clicked.connect(lambda: chooseFile(self))
    self.ui.pushButton.clicked.connect(lambda: recargar_puntaje(self))
    
def setup_photo(self):
    # Configura la foto de perfil del usuario en la interfaz
    try:
        login = get_session()
        photo = db_logic.get_user_photo(login)
        self.ui.profile_picture.setPixmap(QtGui.QPixmap(photo[0]))
    except Exception as e:
        print("Error al configurar la foto:", e)

def setup_profile_labels(self):
    # Configura las etiquetas del perfil con información del usuario
    login = get_session()
    user, apellidos = db_logic.get_user_name(login)
    self.ui.label_4.setText(user)
    self.ui.label_7.setText(apellidos)
    puntaje = db_logic.get_user_score()
    self.ui.label_3.setText(str(puntaje))

def setup_lineEdit_styles(self):
    # Configura los estilos de los campos de texto de cambio de contraseña y foto
    self.ui.label_cambiar_contrasena_warning.setText("")
    self.ui.label_cambiar_foto_warning.setText("")
    line_edits = [
        self.ui.lineEdit_cambiar_contrasena,
        self.ui.lineEdit_cambiar_foto
    ]
    for le in line_edits:
        le.setStyleSheet(styles.lineEdit_correctInputStyle)