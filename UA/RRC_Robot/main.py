import subprocess
import pandas as pd
import numpy as np
import sys

# Ruta completa del intérprete de Python dentro del entorno virtual
python_path = ".venv/bin/python3.12"

################################ PARAMETROS ###############################################
NUM_P = 1

KR_lineal = np.linspace(9, 10, 1)  # 0.65
KR_angular = np.linspace(0.07, 0.065, NUM_P) #0.07
KR_deteccion = np.linspace(2.42, 3, NUM_P) #1.45

KT_lineal = np.linspace(10.4, 10.4, NUM_P)        #1.1
KT_angular = np.linspace(0.02, 0.020, NUM_P)    #0.02
KT_deteccion = np.linspace(0.9, 1.1, NUM_P)     # 0.9


# el TRUCO está en meter un KT_frenado que solo afecte al punto final del triangulo 


################################ CREACIÓN ARCHIVO CSV ###############################################

nombre = "datos.csv"


################################ FUNCIONES ###############################################

def existeFila(nombre:str, fila: list) -> bool:
    try:
        df = pd.read_csv(nombre, index_col=0)
    except:
        df = pd.DataFrame(columns=["puntuacion", "KR_Vl", "KR_Wa", "Dtc-", "segm1", "segm3", "segm5",
                                                    "KT_Vl", "KT_Wa", "DtcΔ", "segm2", "segm4", "segm6"])
        df.index.name = "ID" 
        df.to_csv(nombre, index=True)  
    else:
        for _, row in df.iterrows():
            if [row["KR_Vl"], row["KR_Wa"], row["Dtc-"], row["KT_Vl"], row["KT_Wa"], row["DtcΔ"]] == fila:
                return True
        return False


mapa = "prueba"

################################ MAIN ###############################################
for KRv in KR_lineal:
    for KRw in KR_angular:
        for dtcR in KR_deteccion:
            for KTv in KT_lineal:
                for KTw in KT_angular:
                    for dtcT in KT_deteccion:
                        fila = [KRv, KRw, dtcR, KTv, KTw, dtcT]
                        
                        if not existeFila("datos.csv", fila):
                            if mapa == "f1":
                                result = subprocess.run([python_path, "Austria.py",
                                    str(KRv), str(KRw), str(dtcR),
                                    str(KTv), str(KTw), str(dtcT)
                                ])

                            else:
                                # Ejecuta el archivo .py que deseas ejecutar en bucle con parámetros
                                result = subprocess.run([python_path, "P1Launcher.py",
                                    str(KRv), str(KRw), str(dtcR),
                                    str(KTv), str(KTw), str(dtcT)
                                ])
                        else:
                            print("Ya se ha ejecutado anteriormente:", fila)
                            """result = subprocess.run([python_path, "P1Launcher.py",
                                str(KRv), str(KRw), str(dtcR),
                                str(KTv), str(KTw), str(dtcT)
                            ])"""
                            continue