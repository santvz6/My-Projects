import pandas as pd
import matplotlib.pyplot as plt

from fuzzy_system import evaluar_paciente_difuso
from fuzzy_system import presion_sist, presion_diast, colesterol, glucosa, edad, imc, tabaquismo, alcohol, actividad, riesgo
from patient_input import procesar_fila


GUARDAR_FUNCIONES = False
ANALIZAR_CSV = True


########################## GUARDADO DE FUNCIONES DE PERTENENCIA
if GUARDAR_FUNCIONES:

    functions_path = "functions/"
    funciones = [presion_sist, presion_diast, colesterol, glucosa, edad, imc, 
                tabaquismo, alcohol, actividad, riesgo]

    for funcion in funciones:
        fig, ax = plt.subplots()
        for label in funcion.terms:
            mf = funcion.terms[label].mf
            ax.plot(funcion.universe, mf, label=label)
        
        ax.set_title(f"Funciones de pertenencia - {funcion.label}")
        ax.set_xlabel(funcion.label)
        ax.set_ylabel("Grado de pertenencia")
        ax.legend()
        
        # Guardar como imagen
        plt.savefig(f"{functions_path + funcion.label}.png")
        plt.close(fig)


########################## ANALIZAR CSV
if ANALIZAR_CSV:
    csv_data_path = "csv_data/"
    csv_result_path = "csv_result/"
    csv_name = "test2"


    # Cargamos CSV
    df = pd.read_csv(csv_data_path + csv_name + ".csv", delimiter=";")

    # Evaluamos cada paciente y añadimos una COLUMNA DE RIESGO ESTIMADO
    riesgos_estimados = []
    i = 0

    for _, row in df.iterrows():
        i += 1
        print(i)
        entrada = procesar_fila(row)
        riesgo = evaluar_paciente_difuso(entrada)
        riesgos_estimados.append(riesgo)

    df["RIESGO_ESTIMADO"] = riesgos_estimados

    # Mostrar resultados
    print(df[["AGE", "AP_HIGH", "CHOLESTEROL", "GLUCOSE", "RIESGO_ESTIMADO"]].head())

    # Guardar resultado 
    df.to_csv(csv_result_path + csv_name + ".csv", index=False)



