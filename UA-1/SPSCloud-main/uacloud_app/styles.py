lineEdit_incorrectInputStyle = (
    "  border: 2px solid red;         /* Color de borde (rojo) y ancho (2px) */\n"
    "  border-radius: 10px;           /* Esquinas redondeadas con un radio de 10px */\n"
    "  padding: 5px 10px;             /* Relleno alrededor del texto: 5px arriba/abajo, 10px izquierda/derecha */\n"
    "  background-color: white;       /* Color de fondo blanco */\n"
    "  color: #333333;                /* Color del texto (gris oscuro) */\n"
    "  font-size: 14px;               /* Tamaño de fuente establecido en 14px */\n"
)

lineEdit_correctInputStyle = """
QLineEdit {
    background-color: white;         /* Color de fondo blanco */
    border: 1px solid #d4d4d4;       /* Color de borde (gris claro) y ancho (1px) */
    border-radius: 10px;             /* Esquinas redondeadas con un radio de 10px */
    padding: 5px 10px;               /* Relleno alrededor del texto: 5px arriba/abajo, 10px izquierda/derecha */
    font: 14px;                      /* Tamaño de fuente establecido en 14px */
    color: #333333;                  /* Color del texto (gris oscuro) */
}

QLineEdit:focus {
    border-color: #04D374;           /* Cambiar el color del borde a verde cuando está enfocado */
}

QLineEdit:disabled {
    background-color: #f3f3f3;       /* Color de fondo más claro cuando está deshabilitado */
    border-color: #e0e0e0;           /* Color de borde más claro cuando está deshabilitado */
}
"""
