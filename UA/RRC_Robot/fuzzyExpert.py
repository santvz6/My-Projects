from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from segmento import *
import pandas as pd
import math


class FuzzySystem:
    def __init__(self) -> None:

        self.segmentoObjetivo = None    # Inicializamos valores en P1Launcher
        self.objetivoAlcanzado = False  # Final del segmento
        self.inicioAlcanzado = False    # Inicio del segmento (Punto cercano: Recta, PuntoMedio: Triángulo)
        self.tipoSegmento: str = "recta" # Comenzamos como una recta siempre

        self.KR_deteccion = 2
        self.KT_deteccion = 0.01

        self.poseRobot = ("xRob", "yRob", "angRob", "vR", "wR")

    ######################################### variables
        self.variables: dict = {
            "error_angular": FuzzyVariable(
                universe_range=(0, 180),
                terms={
                    "grande": [(85, 0), (120, 0.33), (140, 0.66), (180, 1)],
                    "medio": [(10, 1), (15, 0.66), (30, 0.33), (90, 0)],
                    "pequeño": [(2, 1), (4, 0.66), (6, 0.33), (10, 0)],
                },
            ),
            "distancia": FuzzyVariable(
                universe_range=(0.5, 100),
                terms={
                    "lejos": [(3, 0), (7, 0.33), (20, 0.66), (25, 1)],
                    "cerca": [(0, 1), (2, 1), (3, 0.66), (4, 0)],
                },
            ),
            "v_lineal": FuzzyVariable(
                universe_range=(0, 3),
                terms={
                    "rapido": [(3, 0), (3, 0.66), (3, 1), (3, 1)],
                    "medio":  [(2.8, 1), (3, 0.66), (3, 0.4), (3, 0)],
                    "lento":  [(0, 1), (0.1, 0.66), (0.5, 0.33), (0.8, 0)],
                    
                },
            ),
            "w_angular": FuzzyVariable(
                universe_range=(0, 3),
                terms={
                    "rapido": [(1.2, 0), (1.4, 0.33), (1.8, 0.66), (2.2, 1)],
                    "medio": [(1.4, 1), (1, 0.66), (0.6, 0.33), (0.4, 0)],
                    "lento": [(0, 1), (0, 0.66), (0.05, 0.33), (0.08, 0)],
                    
                },
            ),
        }

    ######################################### reglas
        self.rules: list[object] = [
            
        ### LEJOS Y BIEN ORIENTADO
            FuzzyRule(
                premise=[
                    ("error_angular", "pequeño"),
                    ("AND", "distancia", "lejos"),
                ],
                consequence=[("v_lineal", "rapido"), ("w_angular", "lento")],
            ),
        ### LEJOS Y NORMAL ORIENTADO
            FuzzyRule(
            
                premise=[
                    ("error_angular", "medio"),
                    ("OR", "error_angular", "grande"),
                    ("AND", "distancia", "lejos"),
                ],
                consequence=[("v_lineal", "rapido"), ("w_angular", "rapido")],
            ),        
        ### LEJOS Y MAL ORIENTADO
            FuzzyRule(
                premise=[
                    ("error_angular", "grande"),
                    ("AND", "distancia", "lejos"),
                ],
                consequence=[("v_lineal", "medio"), ("w_angular", "rapido")],
            ),


        ### CERCA Y BIEN ORIENTADO
            FuzzyRule(
                premise=[
                    ("error_angular", "pequeño"),
                    ("AND", "distancia", "cerca"),
                ],
                consequence=[("v_lineal", "rapido"), ("w_angular", "lento")],
            ),

        ### CERCA Y NORMAL ORIENTADO
            FuzzyRule(
                premise=[
                    ("error_angular", "medio"),
                    ("AND", "distancia", "cerca"),
                ],
                consequence=[("v_lineal", "medio"), ("w_angular", "medio")],
            ),

        ### CERCA Y MAL ORIENTADO
            FuzzyRule(
                premise=[
                    ("error_angular", "grande"),
                    ("AND", "distancia", "cerca"),
                ],
                consequence=[("v_lineal", "lento"), ("w_angular", "rapido")],
            ),
        ]

    def calcularErrorAngular(self, objetivo:tuple) -> float:
        
        xObj, yObj = objetivo
        xRob, yRob, angRob, _, _ = self.poseRobot

        # Calcular el ángulo hacia el punto objetivo
        # tg(ang) = Copuesto / Ccontiguo = y/x
        angulo_objetivo = math.degrees(math.atan2(yObj - yRob, xObj - xRob))
        # Rango [0, 360)
        angulo_robot = angRob % 360 

        # Ángulo entre el Objetivo y el Robot
        error_angular = angulo_objetivo - angulo_robot

        # Si tiene que dar más de media vuelta a la derecha
        # Hacemos que vaya a la izquierda restando -360 (camino más corto)
        if error_angular > 180:
            error_angular -= 360
        # Si tiene que dar más de media vuelta a la izquierda
        # Hacemos que vaya a la derecha sumando +360 (camino más corto)
        elif error_angular < -180:
            error_angular += 360
        
        return error_angular
    
    def tomarDecision(self, poseRobot:tuple) -> tuple:
        """
        Determina que velocidad lineal y angular tiene el robot en el instante de 
        tiempo actual en función de las características del segmentoObjetivo.

        Return
        ------

        Devuelve una tupla con la velocidad lineal y velocidad angular.
        """

        self.poseRobot = poseRobot
        _, _, _, vR, wR = self.poseRobot

        if self.tipoSegmento == "recta":
            error_angular, distancia =  self.decisionRecta()
        else:
            error_angular, distancia = self.decisionTriangulo()
        

    ######################################### evaluación de reglas
        model = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

    ######################################### resultado
        result = model(
            variables=self.variables,
            rules=self.rules,
            error_angular=abs(error_angular),
            distancia=distancia,
            v_lineal=vR,
            w_angular=wR,
        )

        if error_angular > 0:
            return result[0]["v_lineal"], result[0]["w_angular"]
        else:
            return result[0]["v_lineal"], -result[0]["w_angular"]

    def decisionRecta(self) -> tuple:

    #### VARIABLES DEL MÉTODO

        # Información sobre el Robot
        xRob, yRob, _, vRob, _ = self.poseRobot

        # Primer Objetivo: Punto más cercano recta AB respecto al robot R
        # Siguientes Objetivos: Punto (interpolado a una distancia de t)situado en AB entre el punto final B y el robot R
        objetivo = self.puntoCercano() if not self.inicioAlcanzado else self.puntoInterpolado(t=1/9)

        # Diferencia de angulos entre el angObjetivo y el angRobot
        error_angular = self.calcularErrorAngular(objetivo)

        
    #### DETECCIÓN OBJETIVO INICIAL (PUNTO CERCANO)
        distanciaObjetivo = math.sqrt(abs((xRob - objetivo[0]) ** 2 + (yRob - objetivo[1]) ** 2))

        # No es necesario utilizar 0.5 como distancia de detección para el puntoCercano()
        # Utilizamos la fórmula del MRUA para despejar x: v**2 = vo**2 + 2ax 
        # Despejando: -vo**2 / 2a (acelaración negativa = -1) -> vo**2 / 2
        if not self.inicioAlcanzado and distanciaObjetivo <= (vRob**2 + self.KR_deteccion)/2:
            self.inicioAlcanzado = True 

    #### DETECCIÓN OBJETIVO FINAL
        xFinal, yFinal = self.segmentoObjetivo.getFin()
        distanciaFinal = math.sqrt((xRob - xFinal) ** 2 + (yRob - yFinal) ** 2)

        # Sí es necesario utilizar 0.5 como distancia de detección para el puntoFinal()
        if distanciaFinal <= 0.5:
            self.setobjetivoAlcanzado()
        
        distanciaDevuelta = distanciaObjetivo if not self.inicioAlcanzado else distanciaFinal
        return error_angular, distanciaDevuelta

    def decisionTriangulo(self) -> float:

    #### VARIABLES DEL MÉTODO

        # Información sobre el Robot
        xRob, yRob, _, vRob, _ = self.poseRobot

        # Primer Objetivo: Punto Medio del triángulo
        # Segundo Objetivo: Fin del tríangulo
        objetivo = self.segmentoObjetivo.getMedio() if not self.inicioAlcanzado else self.segmentoObjetivo.getFin()
        
        # Diferencia de angulos entre el angObjetivo y el angRobot
        error_angular = self.calcularErrorAngular(objetivo)
        

    #### DETECCIÓN OBJETIVO INICIAL (PUNTO CERCANO)
        if not self.inicioAlcanzado:

            distanciaObjetivo = math.sqrt((xRob - objetivo[0]) ** 2 + (yRob - objetivo[1]) ** 2)
            
            # En este caso hemos añadido, además de la constante de Deteccion
            # La velocidad del robot para ser más precisos cuándo alcanza el objetivo
            if distanciaObjetivo < abs(vRob**2 + self.KT_deteccion*vRob)/2: 
                self.inicioAlcanzado = True

    #### DETECCIÓN OBJETIVO FINAL
        xFinal, yFinal = self.segmentoObjetivo.getFin()
        distanciaFinal = math.sqrt((xRob - xFinal) ** 2 + (yRob - yFinal) ** 2)

        if distanciaFinal <= 0.5:
            self.setobjetivoAlcanzado()

        distanciaDevuelta = distanciaObjetivo if not self.inicioAlcanzado else distanciaFinal
        return error_angular, distanciaDevuelta


#################################### objetivos 

    def puntoCercano(self):

        xRob, yRob, _, _, _ = self.poseRobot
        xA, yA = self.segmentoObjetivo.getInicio()
        xB, yB = self.segmentoObjetivo.getFin()

        # Vectores (AB y AR)
        ABx, ABy = xB - xA, yB - yA
        ARx, ARy = xRob - xA, yRob - yA

        # Proyección de AR sobre AB 
        # Fŕomula utilizada: proyección = AR * AB / |AB|**2

        # Cálculo de |AB| ** 2
        AB_escalar = ABx**2 + ABy**2
        
        try:
            # Cálculo completo y Limitamos el valor en el rango de [0, 1]
            # Dónde 0 es el inicio del segmento y 1 es el final del segmento
            proyeccion_min = min(1, (ARx * ABx + ARy * ABy) / AB_escalar)
            proyeccion = max(0, proyeccion_min)

        except (ZeroDivisionError, ValueError):
            proyeccion = 0 # En caso de cualquier problema

    
        añadidoX, añadidoY = proyeccion * ABx, proyeccion * ABy

        puntoCercanoX = xA + añadidoX
        puntoCercanoY = yA + añadidoY

        return (puntoCercanoX, puntoCercanoY)
        
    def puntoInterpolado(self, t: float):
        
        xC, yC = self.puntoCercano()
        xB, yB = self.segmentoObjetivo.getFin()

        # Fórmula utilizada: P = (1−t)⋅A + t⋅B
        # Dónde A (puntoCercano) tiene más peso que B (puntoFinal)
        añadidoCercanoX, añadidoCercanoY = (1 - t) * xC, (1 - t) * yC
        añadidoFinalX, añadidoFinalY = t * xB, t * yB
        
        puntoInterpoladoX =  añadidoCercanoX + añadidoFinalX
        puntoInterpoladoY =  añadidoCercanoY + añadidoFinalY

        return (puntoInterpoladoX, puntoInterpoladoY)

#################################### P1Launcher 
    def setObjetivo(self, segmento: object) -> None:
        """
        Establece un nuevo segmento Objetivo y resetea los checkpoints
        """
        self.inicioAlcanzado = False
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento

        self.tipoSegmento: str = "recta" if self.segmentoObjetivo.getType() == 1 else "triangulo"

    def setobjetivoAlcanzado(self) -> None:
        self.objetivoAlcanzado = True  

    def hayParteOptativa(self) -> bool:
        return True  
    
    def esObjetivoAlcanzado(self) -> bool:
        return self.objetivoAlcanzado
    
#################################### csv 

# Esta sección la utilicé para hacer diferentes pruebas con distintos parámetros
    def añadirFila(self,nueva_fila: dict, nombre: str) -> None:
            df = pd.read_csv(nombre, index_col=0)
            df.loc[len(df)] = nueva_fila
            df.to_csv(nombre, index=True)
    
    def getmaxID(self, nombre:str) -> int:
        try:
            df = pd.read_csv(nombre, index_col=0)
        except:
            print("getDF(): No hemos podido abrir", nombre)
        else:
            return (max(df.index))