from segmento import *
import pandas as pd
import math

class ExpertSystem:
    def __init__(self) -> None:

        """
        Variables constantes
        ----------
        KR_lineal: constante que determina la velocidad lineal en una recta
        KR_angular: constante que determina la velocidad angular en una recta
        KR_deteccion: determina a partir de que momento el robot detecta un objetivo como alcanzado en una recta

        KT_lineal: constante que determina la velocidad lineal en un triángulo
        KT_angular: constante que determina la velocidad angular en un triángulo
        KT_deteccion: determina a partir de que momento el robot detecta un objetivo como alcanzado en un triángulo

        """
        
        self.segmentoObjetivo = None    # Inicializamos valores en P1Launcher
        self.objetivoAlcanzado = False  # Final del segmento
        self.inicioAlcanzado = False    # Inicio del segmento (Punto cercano: Recta, PuntoMedio: Triángulo)
        self.tipoSegmento: str = "recta" # Comenzamos como una recta siempre

        self.KR_lineal = 10.0     
        self.KR_angular = 0.07
        self.KR_deteccion = 2.42

        self.KT_lineal = 0.02
        self.KT_angular = 0.02
        self.KT_deteccion = 0.9

        self.poseRobot = ("xRob", "yRob", "angRob", "vR", "wR")

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
        tiempo actual y en función de las características del segmentoObjetivo.

        Return
        ------
        Devuelve una tupla con la velocidad lineal y velocidad angular.
        """
        self.poseRobot = poseRobot

        if self.tipoSegmento == "recta":
            return self.decisionRecta()
        else:
            return self.decisionTriangulo()
        
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
        if not self.inicioAlcanzado and distanciaObjetivo <= (vRob**2 - self.KR_deteccion)/2:
            self.inicioAlcanzado = True 

    #### DETECCIÓN OBJETIVO FINAL
        xFinal, yFinal = self.segmentoObjetivo.getFin()
        distanciaFinal = math.sqrt((xRob - xFinal) ** 2 + (yRob - yFinal) ** 2)

        # Sí es necesario utilizar 0.5 como distancia de detección para el puntoFinal()
        if distanciaFinal <= 0.5:
            self.setobjetivoAlcanzado()


    #### V_LINEAL

        # Función matemática utilizada: KR_lineal / sqrt(x=error_angular) 
        # Donde la constante aumenta el valor de la Y respecto de X
        # Se recomienda un valor de 10 para entrar en rango: [≈0.75, inf]
        # Cuando el error_angular es 0 otrogamos una velocidad máxima [3]
        try:
            
            v_lineal = self.KR_lineal/math.sqrt(abs(error_angular)) 
        except (ZeroDivisionError, ValueError):
            
            v_lineal = 3


    #### W_ANGULAR

        # Función matemática utilizada: sqrt(x=error_angular) * KR_angular
        # Donde la constante aumenta el valor de la Y respecto de X
        # Se recomienda un valor de 0.07 para entrar en el rango de [0, 1]
        # No buscamos w_angulares muy altas en rectas

        try:
            w_angular =  math.sqrt(error_angular) * self.KR_angular if error_angular >= 0 else -math.sqrt(-error_angular) * self.KR_angular 

        except (ValueError):
            w_angular = 0 # utilizado por si ocurre algún problema inesperado
  
        return v_lineal, w_angular

    def decisionTriangulo(self) -> tuple:

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
            if distanciaObjetivo < abs(vRob**2 - self.KT_deteccion*vRob)/2: 
                self.inicioAlcanzado = True

    #### DETECCIÓN OBJETIVO FINAL
        xFinal, yFinal = self.segmentoObjetivo.getFin()
        distanciaFinal = math.sqrt((xRob - xFinal) ** 2 + (yRob - yFinal) ** 2)

        if distanciaFinal <= 0.5:
            self.setobjetivoAlcanzado()

    #### V_LINEAL

        # La velocidad siempre tendrá el valor de 3
        # cuando el error angular es mayor de 120 el valor de la función comienza a disminuir 
        # La velocidad de decrecimiento viene dada por la constante KT_lineal
        v_lineal = 3 - ((error_angular-120) * self.KT_lineal)
 

    #### W_ANGULAR
        w_angular = self.KT_angular * error_angular

        return v_lineal, w_angular

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