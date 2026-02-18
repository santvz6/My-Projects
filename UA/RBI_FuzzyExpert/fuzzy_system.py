import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
# ------------------
# 1) Definición de variables
# ------------------
presion_sist = ctrl.Antecedent(np.arange(60, 241, 1), 'presion_sist')
presion_diast = ctrl.Antecedent(np.arange(40, 191, 1), 'presion_diast')
colesterol = ctrl.Antecedent(np.arange(1, 4, 1), 'colesterol')
glucosa = ctrl.Antecedent(np.arange(1, 4, 1), 'glucosa')
edad = ctrl.Antecedent(np.arange(30, 66, 1), 'edad')
imc = ctrl.Antecedent(np.arange(10, 60, 0.5), 'imc')
tabaquismo = ctrl.Antecedent(np.arange(0, 2, 1), 'tabaquismo')
alcohol = ctrl.Antecedent(np.arange(0, 2, 1), 'alcohol')
actividad = ctrl.Antecedent(np.arange(0, 2, 1), 'actividad')
riesgo = ctrl.Consequent(np.arange(0, 11, 1), 'riesgo')
# ------------------
# 2) Funciones de membresía
# ------------------
# Presión sistólica (alta)
presion_sist['normal']   = fuzz.trapmf(presion_sist.universe, [60,  90, 110, 130]) 
presion_sist['alta']     = fuzz.trapmf(presion_sist.universe, [120, 125,130, 140])
presion_sist['muy alta'] = fuzz.trapmf(presion_sist.universe, [130, 150,240, 300]) # 300 fuera de rango -> pertenencia total (no finaliza bajando)
# Presión diastólica (baja)
presion_diast['normal']   = fuzz.trapmf(presion_diast.universe, [40,  60, 80,  90])
presion_diast['alta']     = fuzz.trapmf(presion_diast.universe, [80,  90, 110, 120])
presion_diast['muy alta'] = fuzz.trapmf(presion_diast.universe, [110, 120,180, 200]) # 200 fuera de rango -> pertenencia total (no finaliza bajando)
presion_diast['muy alta'] = fuzz.trapmf(presion_diast.universe, [110, 120,191, 200]) # 200 fuera de rango -> pertenencia total (no finaliza bajando)

# Colesterol
colesterol['bueno']  = fuzz.trimf(colesterol.universe, [1, 1, 2])
colesterol['medio']  = fuzz.trimf(colesterol.universe, [1, 2, 3])
colesterol['malo']   = fuzz.trimf(colesterol.universe, [2, 3, 3])

# Glucosa
glucosa['buena']  = fuzz.trimf(glucosa.universe, [1, 1, 2])
glucosa['media']  = fuzz.trimf(glucosa.universe, [1, 2, 3])
glucosa['mala']   = fuzz.trimf(glucosa.universe, [2, 3, 3])

# Edad
edad['joven']  = fuzz.trimf(edad.universe, [30, 35, 45])
edad['joven']  = fuzz.trapmf(edad.universe, [0, 30, 35, 45]) # 0 fuera de rango
edad['media']  = fuzz.trimf(edad.universe, [40, 50, 60])
edad['mayor']  = fuzz.trimf(edad.universe, [55, 60, 65])
edad['mayor']  = fuzz.trapmf(edad.universe, [55, 60, 65, 100]) # 100 fuera de rango

# IMC
imc['bajopeso']  = fuzz.trapmf(imc.universe, [5,  10, 16.5, 19]) # 5 fuera de rango
imc['normal']    = fuzz.trapmf(imc.universe, [18, 19, 24,   24.9])
imc['sobrepeso'] = fuzz.trapmf(imc.universe, [25, 26, 29,   29.9])
imc['obeso']     = fuzz.trapmf(imc.universe, [30, 35, 60,   70]) # 70 fuera de rango 
# Tabaquismo, Alcohol, Actividad
for var in (tabaquismo, alcohol, actividad):
    var['no'] = fuzz.trimf(var.universe, [0, 0, 1])
    var['si'] = fuzz.trimf(var.universe, [0, 1, 1])
# Riesgo
riesgo['bajo']      = fuzz.trimf(riesgo.universe, [0, 2,  5])
riesgo['moderado']  = fuzz.trimf(riesgo.universe, [3, 6,  8])
riesgo['alto']      = fuzz.trimf(riesgo.universe,  [5, 10, 10])
# ------------------
# 3) Reglas difusas específicas
# ------------------
rules = [
    
    # Alto riesgo
    ctrl.Rule(presion_sist['muy alta'] | presion_diast['muy alta'], riesgo['alto']),
    ctrl.Rule(colesterol['malo'] | glucosa['mala'], riesgo['alto']),
    ctrl.Rule(imc['obeso'] & edad['mayor'], riesgo['alto']),
    ctrl.Rule(tabaquismo['si'] & alcohol['si'], riesgo['alto']),
    ctrl.Rule(tabaquismo['si'] & edad['mayor'], riesgo['alto']),
    ctrl.Rule(actividad['no'] & imc['obeso'], riesgo['alto']),
    # Regla ajustada para aumentar la relevancia de la edad
    ctrl.Rule(edad['mayor'] & (presion_sist['normal'] | presion_diast['normal']), riesgo['alto']),
    ctrl.Rule(edad['mayor'] & colesterol['medio'], riesgo['alto']),
    ctrl.Rule(edad['mayor'] & glucosa['media'], riesgo['alto']),
    ctrl.Rule(edad['mayor'] & imc['normal'], riesgo['alto']),
    # Reglas ajustadas con más énfasis en presión
    ctrl.Rule(presion_sist['alta'] & presion_diast['alta'], riesgo['alto']),
    ctrl.Rule(presion_sist['muy alta'] & presion_diast['normal'], riesgo['alto']),
    ctrl.Rule(imc['obeso'] & tabaquismo['si'], riesgo['alto']),
    
    # Bajo riesgo
    ctrl.Rule(actividad['si'] & presion_sist['normal'] & presion_diast['normal'] & 
              colesterol['bueno'] & glucosa['buena'] & imc['normal'], riesgo['bajo']),
    ctrl.Rule(actividad['si'] & presion_sist['normal'] & colesterol['bueno'], riesgo['bajo']),
    ctrl.Rule(actividad['no'] & colesterol['bueno'], riesgo['bajo']),
    ctrl.Rule(presion_sist['normal'] & imc['normal'], riesgo['bajo']),
    # Reglas para mayor edad con condiciones moderadas
    ctrl.Rule(edad['mayor'] & imc['sobrepeso'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & actividad['no'], riesgo['moderado']),
    
    # Riesgo moderado
    ctrl.Rule(imc['sobrepeso'] & edad['media'], riesgo['moderado']),
    ctrl.Rule(colesterol['medio'] | glucosa['media'], riesgo['moderado']),
    ctrl.Rule(imc['sobrepeso'] & glucosa['media'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & ~presion_sist['muy alta'] & ~presion_diast['muy alta'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & colesterol['medio'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & glucosa['media'], riesgo['moderado']),
    # Ajustes para moderado considerando más factores
    ctrl.Rule(edad['media'] & colesterol['medio'], riesgo['moderado']),
    ctrl.Rule(edad['media'] & imc['sobrepeso'], riesgo['moderado']),
    # Reglas moderadas ajustadas con énfasis en la edad
    ctrl.Rule(imc['sobrepeso'] & edad['media'], riesgo['moderado']),
    ctrl.Rule(colesterol['medio'] | glucosa['media'], riesgo['moderado']),
    ctrl.Rule(imc['sobrepeso'] & glucosa['media'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & ~presion_sist['muy alta'] & ~presion_diast['muy alta'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & colesterol['medio'], riesgo['moderado']),
    ctrl.Rule(edad['mayor'] & glucosa['media'], riesgo['moderado']),
    # Reglas para edad joven (30-40 años)
    ctrl.Rule(edad['joven'] & (presion_sist['normal'] | presion_diast['normal']), riesgo['bajo']),
    ctrl.Rule(edad['joven'] & colesterol['bueno'], riesgo['bajo']),
    ctrl.Rule(edad['joven'] & glucosa['buena'], riesgo['bajo']),
    ctrl.Rule(edad['joven'] & imc['normal'], riesgo['bajo']),
    ctrl.Rule(edad['joven'] & (presion_sist['alta'] | presion_diast['alta']), riesgo['moderado']),
    
    # Reglas para pacientes jóvenes con factores de riesgo
    ctrl.Rule(edad['joven'] & colesterol['malo'], riesgo['moderado']),
    ctrl.Rule(edad['joven'] & glucosa['mala'], riesgo['moderado']),
    ctrl.Rule(edad['joven'] & imc['sobrepeso'], riesgo['moderado']),
    ctrl.Rule(edad['joven'] & tabaquismo['si'], riesgo['moderado']),
    # Reglas para pacientes de edad media con factores de riesgo
    ctrl.Rule(edad['media'] & colesterol['malo'], riesgo['alto']),
    ctrl.Rule(edad['media'] & glucosa['mala'], riesgo['alto']),
    ctrl.Rule(edad['media'] & imc['obeso'], riesgo['alto']),
]
# ------------------
# 4) Regla “por defecto” que cubre absolutamente cualquier combinación
# ------------------
# Esta regla utiliza la unión de TODOS los conjuntos difusos de cada variable,
# de modo que si ninguna regla específica dispara, siempre tendremos riesgo moderado.
rules.append(
    ctrl.Rule(
        (presion_sist['normal']  | presion_sist['alta']  | presion_sist['muy alta']) &
        (presion_diast['normal'] | presion_diast['alta'] | presion_diast['muy alta']) &
        (colesterol['bueno']     | colesterol['medio']   | colesterol['malo']) &
        (glucosa['buena']        | glucosa['media']      | glucosa['mala']) &
        (edad['joven']           | edad['media']         | edad['mayor']) &
        (imc['bajopeso']         | imc['normal']         | imc['sobrepeso'] | imc['obeso']) &
        (tabaquismo['no']        | tabaquismo['si']) &
        (alcohol['no']           | alcohol['si']) &
        (actividad['no']         | actividad['si']),
        riesgo['moderado'],
        label='default_moderado'
    )
)
# ------------------
# 5) Sistema y función de evaluación
# ------------------
sistema_control = ctrl.ControlSystem(rules)
def evaluar_paciente_difuso(paciente):
    
    sim = ctrl.ControlSystemSimulation(sistema_control)
    for key, val in paciente.items():
        sim.input[key] = val
    
    try:
        sim.compute()   
        if 'riesgo' not in sim.output:
            return 5.0  # Valor por defecto si no se calcula correctamente
        return sim.output['riesgo']
    
    except Exception as e:
        return 5.0 