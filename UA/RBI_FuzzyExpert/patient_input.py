def procesar_fila(row):
    return {
        'edad': row['AGE'],
        'presion_sist': row['AP_HIGH'],
        'presion_diast': row['AP_LOW'],
        'colesterol': row['CHOLESTEROL'],
        'glucosa': row['GLUCOSE'],
        'imc': (row['WEIGHT'] / (row['HEIGHT'] / 100) ** 2), # Cálculo IMC
        'tabaquismo': row['SMOKE'],
        'alcohol': row['ALCOHOL'],
        'actividad': row['PHYSICAL_ACTIVITY']
    }

