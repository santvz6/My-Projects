import pygame, random, math, sys,time
from pygame.locals import *
from pygame.sprite import Group

#import SPSCloud_app.db.db_logic as db_logic
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../SPSCloud_app')

import db.db_logic as db_logic
import config

############################# PANTALLA #############################
ANCHO = 800
ALTO = 600
FPS = 60  

############################# COLORES #############################
NEGRO = (0,0,0)
BLANCO = (255,255,255)

GRIS = (122,122,122)

ROJO = (255,0,0)
ROJO1 = (102,0,34)
ROJO2 = (160,0,0)

VERDE= (0,255,0)
VERDE1 = (0,160,0)
VERDE2 = (0,102,0)
VERDE3 = (0,55,0)

AZUL = (0,0,255)
AZUL1 = (0,0,160)

AMARILLO = (255,255,0)
AMARILLO1 = (160,160,0)
NARANJA = (255,140,0)

azul_t = (0,131,234,50)
lila_t = (201,131,234,50)
rojo_t = (255,0,0,20)
verde_t = (0,255,0,20)
gris_t = (200,200,200,100)
trans = (0,0,0,0)


#####################################################################
locate = 0  # 0:INICIO BIRDY | 1:BIRDY JUEGO | 2:PAUSA BIRDY | 3:DIFICULTAD BIRDY
#####################################################################

#############################################################################
#                               VARIABLES GLOBALES                          #
#############################################################################

######################################## INICIO BIRDY SWORD ########################################
col1_birdy = BLANCO
col2_birdy = BLANCO
col3_birdy = BLANCO
bot_esp1 = 0
bot_esp2 = 0

######################################## BIRDY SWORD ########################################
saltar = False
puntuacion = 0 
dificultad_birdy = 1 # 3 FÁCIL, 2 NORMAL, 1 DIFÍCIL

x = 0  # FONDO MOVIMIENTO

### VARIABLES DE CONTADOR ###
conteo_musica = 0 

conteo_animacion = 0
cambio_animacion = 0.1

conteo_animacion2 = 0
cambio_animacion2 = 0.05

conteo_2segundos = 0 # conteo cada 2 segundos

reinicio_textoflotante = 0
texto_flotante = '' # texto al pillar una habilidad

cooldown_hab = 10 # cada cuantos segundos sale una habilidad
tipo_habilidad = -1 # Está variable definirá el tipo de habilidad generada

conteo_Msegundo = 0 # conteo cada medio segundo

conteo_1segundos = 0
conteo_animar = 0

######################################## DINERO ########################################
conversor = False
dinero = 0

##########################################################################
#                               INICIADOR                                #
##########################################################################

pygame.init()

# AJUSTES PANTALLA
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SPS CLOUD")
clock = pygame.time.Clock()

############################# CARGA DE SPRITES #############################

moneda_animada = [pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m1.png').convert(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m2.png').convert(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m3.png').convert(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m4.png').convert(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m5.png').convert(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/monedas/m6.png').convert()]

espada_animada = [pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/espadas/e1.png').convert_alpha(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/espadas/e2.png').convert_alpha(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/espadas/e3.png').convert_alpha(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/espadas/e4.png').convert_alpha(),
                  pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/espadas/e5.png').convert_alpha()]

fondo = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/fondo.png').convert()
menu_birdy = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/birdy_menu.png').convert()

pajaro = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/jugador/pajaro.png').convert()
pajaro_animado = pygame.transform.scale(pajaro,(pajaro.get_width()- 71,49))

sp_habilidad = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/obstaculos/mistery_box/box.png').convert() #SPRITE DE MISTERY BOX


############################# CARGA DE CANCIONES #############################
canciones = ['../SPSCloud_app/juegos/flappy_bird/musica/dry_hands.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/wet_hands.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/sweden.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/mice_on_venus.mp3']

#######################################################################################
#                                        FUNCIONES                                    #
#######################################################################################

def reproducir_cancion(cancion):
    pygame.mixer.music.load(cancion) # Cargar la canción seleccionada
    pygame.mixer.music.play() # Reproducir la canción que se cargó

def FondoMovimiento(fondo):
    global x # Dado que si ponemos x=0 y lo usamos en un bucle estaría reiniciando la x todo el rato

    x_relativa = x % fondo.get_rect().width
    pantalla.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < ANCHO:
        pantalla.blit(fondo, (x_relativa, 0))
    x -= 1

def muestra_texto(pantalla, texto, color, x, y, fuente, tamaño_letra):
    fuente = pygame.font.Font(fuente,tamaño_letra) # Carga de fuente
    superficie = fuente.render(texto, True, color) # Generamos una superficie. ORDEN -> Texto, Antialiasing, color
    pantalla.blit(superficie, (x, y)) # Añadimos esta superficie que contiene el texto

def temporizador():
    global conteo_animacion,conteo_animacion2,conteo_1segundos, conteo_2segundos,conteo_animar,conteo_Msegundo
    global cambio_animacion, cambio_animacion2, reinicio_textoflotante
    # tienen que estar fuera para que no los actualice a 0 en el bucle

    tiempo_transcurrido = pygame.time.get_ticks() # 1000 TICKS = 1 SEGUNDO
    if tiempo_transcurrido > (conteo_animacion+1)*(cambio_animacion * 1000): # Cada 0.1seg*1000ticks = 0.1seg * 1 seg
        conteo_animacion +=1                                            # Cada 0.1 seg conteo_animacion suma 1

    if tiempo_transcurrido > (conteo_animacion2+1)*(cambio_animacion2 * 1000): # Principalmente lo usaremos para las espadas
        conteo_animacion2 +=1                                                  # Cada 0.05*1000 = 0.05seg * 1seg. Cambia cada 0.05seg

    if tiempo_transcurrido > (conteo_2segundos+1)*(2000):   # Conteo que suma uno cada 2000ticks = 2 segundos
        conteo_2segundos +=1        # Solo usamos conteo_2segundos para que este conteo siga funcionando
        reinicio_textoflotante += 1     # Define la duracion del texto que se muestra al agarrar una habilidad

    if tiempo_transcurrido > (conteo_1segundos+1)* 1000:
        conteo_1segundos += 1
        conteo_animar += 1

    if tiempo_transcurrido > (conteo_Msegundo + 1) * 500:
        conteo_Msegundo += 1


#######################################################################################
#                       LLAMADA DE FUNCIONES - FUERA DE BUCLE                         #
#######################################################################################
if locate == 1:
    reproducir_cancion(canciones[conteo_musica]) # conteo_musica se va modificando dentro del bucle del juego


#######################################################################################
#    CREACIÓN DE CLASES -> Nos ayuda a modificar cada Objeto en particular            #
####################################################################################### 
class Jugador(pygame.sprite.Sprite):    #  Creamos la clase Jugador 
    def __init__(self): # Función de inicialización. Nos servirá para establecer los ajustes principales.
        super().__init__() 

        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert(),(70,49)) 
        # creamos una variable image que toma el sprite de un rectángulo sólido de 70px * 49 px
        self.image.blit(pajaro_animado,(0,0),pygame.Rect(conteo_animacion%3 * 69, 0, 70, 49)) 
        # mostramos en este rectángulo sólido la imagen del pájaro animado, esta imagen se verá afectada por
        # la posición en la que se encuentre conteo_animacion -> Efecto de movimiento.

        #self.image = pygame.Surface((70,49))   # HITBOX DEL OBJETO JUGADOR
        #self.image.fill(VERDE)
        
        self.rect = self.image.get_rect() # Asignamos a rect el valor del tamaño rectángulo de la Surface/Imagen (self.image)
        self.rect.center = (ANCHO // 3, ALTO // 2) # Posición Inicial del centro del rectángulo obtenido

        self.velocidad_y = 0 # Velocidad Inicial = 0
        self.saltando = False # Estado del Salto inicial -> Falso = Cayendo

    def update(self): # FUNCIÓN DE ACTUALIZACIÓN PARA LAS VARIABLES CREADAS EN EL __init__
    # SE EJECUTA CADA VUELTA DEL BUCLE    
        global saltar # Dado que no quiero usar 'pygame.key.get_pressed()' -> Uso pygame.event y pygame.key en el bucle del juego.
        
        # Por tanto, si se presiona K_SPACE saltar toma el valor de True
        if saltar: 
            self.velocidad_y = -10  # Establece la velocidad hacia arriba
            saltar = False  # Establece saltar False hasta que se presiona K_SPACE

        self.velocidad_y += 0.5 # Aceleración -> Asignamos a la velocidad un aumento 
        self.rect.y += self.velocidad_y # A la posicion se le va sumando el valor de la velocidad(+10px) de forma constante
                                        # Da como resultado un movimiento de  en el eje 'y' cada vuelta del bucle

        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert(),(70,49))
        self.image.blit(pajaro_animado,(0,0),pygame.Rect(conteo_animacion%3 * 70, 0, 70, 49))
        self.image.set_colorkey(VERDE)  # Elimina el CHROMA de la variable imagen con el color deseado

        # MÁRGENES
        if self.rect.y < 0 - self.rect.height: # Si la posición del jugador es menor que los límites de la pantalla, su posición
            self.rect.y = ALTO                 # cambiará al ALTO de la pantalla. De arriba a abajo.

        if self.rect.y > ALTO:                  # Si la posición del jugador es mayor que los límites de la pantalla, 
            self.rect.y = 0 - self.rect.height  # su posición cambiará a 0. De abajo a arriba.
            self.velocidad_y -= 6.8 # Cada vez que aparece arriba establecemos la velocidad a -=6.8 para que no acelere descrontoladamente
 
class Espadas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(espada_animada[conteo_animacion2%5],(60,30))
        self.image.set_colorkey(VERDE)

        #self.image.fill(ROJO) # Visualizar Hitbox

        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

        self.velocidad_x = 9 # Velocidad inicial en el eje 'x'

    def update(self):

        self.velocidad_x = 9
        self.rect.x -= self.velocidad_x # restamos para que la espada vaya hacia la izquierda

        self.image = pygame.transform.scale(espada_animada[conteo_animacion2%5],(60,30))
        self.image.set_colorkey(VERDE)

        if self.rect.x < 0: # Si la espada supera el límite izquierdo se vuelve a generar pero en una altura diferente
            self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

class Monedas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(moneda_animada[conteo_animacion % 6],(40,40)) 
        self.image.set_colorkey(AZUL)

        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(ANCHO, ANCHO+100), random.randint(0, ALTO - self.rect.height))

        self.velocidad_x = 0 # Velocidad inicial

    def update(self):

        self.velocidad_x = 10
        self.rect.x -= self.velocidad_x
        self.image = pygame.transform.scale(moneda_animada[conteo_animacion%6],(40,40))
        self.image.set_colorkey(AZUL) 
   
        if self.rect.x < 0:
            self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

class Habilidad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert(),(70,64))
        self.image.blit(sp_habilidad,(0,0),pygame.Rect(conteo_animacion%8 * 68, 0, 70, 64))
        # SPRITE EN MOVIMIENTO - OPTIMIZACIÓN DE SPRITES - EXPLICACIÓN DEL FUNCIONAMIENTO DE ANIMACIÓN DE SPRITES
        # Tamaño sprite 543 x 64. conteo_animacion suma 1 cada 0.1 segundos. conteo_animacion %8: Cada 0.8 segundos movemos la 'x' 68 pixeles
        # Se mueve cada 0.8 porque conteo suma 1 cada 0.1 seg. Entonces cuando el resto es 1 han pasado 0.8 seg, luego 1.6 para mover 68 px más
        # 0 : posición de la y fija en 0. Tamaño del Rect: (70,64)
        
        self.image.set_colorkey(VERDE)

        self.rect = self.image.get_rect()
        self.rect.topleft = (cooldown_hab * 600, random.randint(0, ALTO - 64))
        #Si va a 10 px por tick = 600px por segundo. Quiero que pase cada 15seg * 600px
 
        self.velocidad_x = 0

    def update(self):
        global cooldown_hab

        self.velocidad_x = 10
        self.rect.x -= self.velocidad_x

        self.image.blit(sp_habilidad,(0,0),pygame.Rect(conteo_animacion%8 * 68, 0, 70, 64))
        self.image.set_colorkey(VERDE)       

        if self.rect.x < 0 - self.rect.width:
            self.rect.topleft = (cooldown_hab*600, random.randint(0, ALTO - 64))
        # Para optimizar y no crear una función de temporizador hacemos que tarde más en reaparecer.
         
############################# CREACIÓN DE GRUPOS -> al añadir un grupo hay que añadir un update #############################
playerG = pygame.sprite.Group()
obstaculoG = pygame.sprite.Group()
monedaG = pygame.sprite.Group()
monedaG_habilidad = pygame.sprite.Group() # Grupo para las monedas generadas por la habilidad
habilidadG = pygame.sprite.Group()


############################# INSTANCIACIÓN DE OBJETOS #############################
jugador = Jugador()
playerG.add(jugador) # añadimos al Grupo player la clase Jugador()

for n in range(0,6):
    espada = Espadas()
    obstaculoG.add(espada) # añadimos al Grupo obstaculo la clase Espadas()

habilidad =  Habilidad()
habilidadG.add(habilidad) # añadimos al grupo Habilidad la clase Habilidad()


ejecutando = True
while ejecutando:
############################################################################################################################
#                                                    BIRDY SWORD MENÚ                                                      #
############################################################################################################################
    if locate == 0:
        clock.tick(FPS) # Velocidad del bucle de juego, en este caso 60 ticks cada vuelta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False  # Finaliza el bucle del juego si presionamos la 'x' de la ventana.

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN

                if 195 < mouse_pos[0] < 375 and 485 < mouse_pos[1] < 540: # Coordenadas del BOTÓN PLAY
                    locate = 3 # nos dirige para elegir la dificultad
                elif 445 < mouse_pos2[0] < 635 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN SALIR
                    puntuacion = 0

                    #pygame.quit()
                    sys.exit()
                    

                #elif 290 < mouse_pos2[0] < 520 and 555 < mouse_pos2[1] < 590: # Coordenadas del BOTÓN DIFICULTAD
                    #locate = 3

        mouse_pos2 = pygame.mouse.get_pos() # Nos devuelve la pos del ratón constantemente

        if 195 < mouse_pos2[0] < 375 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN JUGAR
            col1_birdy = VERDE # Animación de color / Botón jugar
            bot_esp1 += 0.2 # Animación espada
        elif 445 < mouse_pos2[0] < 635 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN SALIR
            col2_birdy = ROJO
            bot_esp2 += 0.2
        #elif 290 < mouse_pos2[0] < 520 and 555 < mouse_pos2[1] < 590: # Coordenadas del BOTÓN DIFICULTAD
            #col3_birdy = NARANJA
        else: # Volver a establecer valores por defecto
            bot_esp1 = 0
            bot_esp2 = 0
            bot_esp3 = 0
            col1_birdy = BLANCO
            col2_birdy = BLANCO
            col3_birdy = BLANCO
        ############### DIBUJO DE SPRITES ###############
        pantalla.blit(pygame.transform.rotate(pygame.transform.scale(espada_animada[int(round(bot_esp1,0))%5],(86.4,42)),220), (172,460))
        pantalla.blit(pygame.transform.rotate(pygame.transform.scale(espada_animada[int(round(bot_esp2,0))%5],(86.4,42)),320), (572,460))

        muestra_texto(pantalla,'JUGAR',NEGRO,200,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',34)
        muestra_texto(pantalla,'JUGAR',col1_birdy,200,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04B.TTF',34)

        muestra_texto(pantalla,'SALIR',NEGRO,450,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',34)
        muestra_texto(pantalla,'SALIR',col2_birdy,450,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04B.TTF',34)
        
        #muestra_texto(pantalla,'DIFICULTAD',NEGRO,300,560,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',21)
        #muestra_texto(pantalla,'DIFICULTAD',col3_birdy,300,560,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04B.TTF',21)    

        ############################# LLAMADA DE FUNCIONES - DENTRO DE BUCLE #############################
        temporizador()
       
        pygame.display.flip()  # Actualiza el contenido de la pantalla.
        FondoMovimiento(menu_birdy) 

############################################################################################################################
#                                                   BIRDY SWORD BUCLE                                                      #
############################################################################################################################

    elif locate == 1:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False 
            if event.type == pygame.KEYDOWN: # Si se presiona (KEYDOWN)...
                if event.key == pygame.K_SPACE: # ...y se presiona la tecla (K_SPACE) -> acción deseada
                    saltar = True               
                if event.key == pygame.K_ESCAPE: # Si presionamos ESC -> locate nos lleva al Menú de pausa
                    locate = 2 # Menú de pausa
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                saltar = True # Incluimos el salto para el click derecho
                    
        
        ################ MÚSICA -> CAMBIO AUTOMÁTICO ################
        if not pygame.mixer.music.get_busy():   # Reproduciendo canción = True / No reproduciendo = False
            if conteo_musica >= len(canciones)-1:   # Si superamos la longitud de la lista se reproduce la primera canción
                conteo_musica = 0
                reproducir_cancion(canciones[conteo_musica])
            else:   # Al no ser el final, pasamos a la siguiente canción
                conteo_musica += 1
                reproducir_cancion(canciones[conteo_musica])

        
        ################ ASIGNACIÓN DE TECLAS - MÚSICA ################
        tecla = pygame.key.get_pressed()
        
        # Bajar volumen
        if tecla[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()- 0.01)
        
        #Subir volumen
        if tecla[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+ 0.01)

        # Mutear
        if tecla[pygame.K_m]:
            pygame.mixer.music.set_volume(0.0)

        
        ################ COLISIONES ################
        # Colisión -> objeto(x) - con - grupo(xG)

        ### JUGADOR - ESPADAS ###
        colision_jugador = pygame.sprite.spritecollide(jugador, obstaculoG, True)   #True hace kill() a la clase cuando colisiona
        if colision_jugador:
            puntuacion -= 1 # Castigamos al jugador restándole uno a su puntuación
            espada = Espadas()  # Como se elimina al colisionar, instanciamos otra espada
            obstaculoG.add(espada)

        ### JUGADOR - MONEDAS ###
        colision_monedas = pygame.sprite.spritecollide(jugador, monedaG, True)
        if colision_monedas: 
            puntuacion += 1 # premiamos al jugador
            moneda = Monedas()
            monedaG.add(moneda)

        ### JUGADOR - HABILIDAD ###
        colision_habilidad = pygame.sprite.spritecollide(jugador, habilidadG, True)
        if colision_habilidad:
            habilidad = Habilidad()
            habilidadG.add(habilidad)
            tipo_habilidad = random.randint(0,2) # Tipo de habilidad generada aleatoriamente
             
            if tipo_habilidad == 0:     # GENERACIÓN MONEDAS ALEATORIAS
                for n in range(random.randint(0,10)): # Instanciamos 0 o 10 monedas en el grupo dedicado a esta habilidad
                    moneda = Monedas() 
                    monedaG_habilidad.add(moneda)   #Grupo dedicado -> monedaG_habilidad -> No se instancia en ningún sitio más
            
            elif tipo_habilidad == 1:     # SUMA DE PUNTOS ALEATORIA
                reinicio_textoflotante = 0  # Este reseteo nos servirá para establecer el contador a 0 más adelante
                suma_resta = random.randint(1,10)   # Cantidad aleatoria que se le añadirá a la puntuación
                puntuacion += suma_resta

            elif tipo_habilidad == 2:   #  RESTA DE PUNTOS ALEATORIA
                reinicio_textoflotante = 0
                suma_resta = random.randint(1,10)
                puntuacion -= suma_resta

        ######## HABILIDAD MONEDAS ########
        # Necesitamos separar las monedas de las monedas generadas por la habilidad
        # Eliminamos y no generamos las monedas generadas por la habilidad (MONEDAS NO INFINITAS)
        colision_habilidad_monedas = pygame.sprite.spritecollide(jugador, monedaG_habilidad, True) 
        if colision_habilidad_monedas:
            puntuacion += 1 # Estas monedas siguen sumando 1

        ######## HABILIDAD SUMA ########
        if tipo_habilidad == 1:     # Lo metemos dentro del bucle, no como justo arriba que solo se ejecuta al colisionar.
                                    # Es una gran diferencia que nos ayudará a controlar los temporizadores.
            if reinicio_textoflotante == 1 or reinicio_textoflotante == 0: # reinicio_textoflotante suma 1 cada 2 segundos (VER def temporizador())
                                                                           # por tanto este if se ejecutaría durante 4 segundos
                texto_flotante = str(suma_resta)    # suma_resta -> cantidad aleatoria que se suma
            else:
                texto_flotante = ''     # Cuando pasan los 4 segundos, el texto se mostrará invisible

            muestra_texto(pantalla,texto_flotante,NEGRO, jugador.rect.x + 10 ,jugador.rect.y - 40,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',30)
            muestra_texto(pantalla,texto_flotante,VERDE,jugador.rect.x + 10 ,jugador.rect.y - 40,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',30)

        ######## HABILIDAD RESTA ########
        if tipo_habilidad == 2:
            if reinicio_textoflotante == 0 or reinicio_textoflotante == 1:
                texto_flotante = '-' + str(suma_resta) # suma_resta -> cantidad aleatoria que se resta
            else:
                texto_flotante = ''

            muestra_texto(pantalla,texto_flotante,NEGRO, jugador.rect.x-10 ,jugador.rect.y - 40,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',30)
            muestra_texto(pantalla,texto_flotante,ROJO,jugador.rect.x-10 ,jugador.rect.y - 40,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',30)

        ############################# ACTUALIZACIÓN DE LOS GRUPOS #############################
        playerG.update()
        obstaculoG.update()
        monedaG.update()
        monedaG_habilidad.update()
        habilidadG.update()

        ############################# DIBUJO DE SPRITES / TEXTOS / FIGURAS #############################
        # pantalla.blit(pygame.image.load('escenario/fondo.png'),(0,0)) -> Fondo estático
        playerG.draw(pantalla)
        obstaculoG.draw(pantalla)
        monedaG.draw(pantalla)
        monedaG_habilidad.draw(pantalla)
        habilidadG.draw(pantalla)

        muestra_texto(pantalla,str(puntuacion),VERDE3,47,ALTO-80,'../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',70)
        muestra_texto(pantalla,str(puntuacion),BLANCO,40,ALTO-80, '../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',70)
        muestra_texto(pantalla,str(round(pygame.mixer.music.get_volume(),2)),BLANCO,750,560,'../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',18)
        muestra_texto(pantalla,'9: BAJAR VOLUMEN',BLANCO,600,550,'../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',13)
        muestra_texto(pantalla,'0: SUBIR VOLUMEN',BLANCO,600,570,'../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',13)
        muestra_texto(pantalla, str(conteo_animacion/10),NEGRO,360,15,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',30)
        muestra_texto(pantalla, str(conteo_animacion/10),BLANCO,360,15,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',30)
        
        ############################# LLAMADA DE FUNCIONES - DENTRO DE BUCLE #############################
        temporizador()        
        pygame.display.flip() # Actualiza el contenido de la pantalla.
        FondoMovimiento(fondo) 

############################################################################################################################
#                                               PAUSA BIRDY SWORD                                                          #
############################################################################################################################
    elif locate==2:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    locate = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                mouse_pos = pygame.mouse.get_pos()
                if 69 < mouse_pos[0] < 371 and 349 < mouse_pos[1] < 451: # Coordenadas 'menú sps cloud'
                    ##### BIRDY SWORD ######
                    dinero += puntuacion
                    puntuacion = 0

                    print(f"Dinero: {dinero}")
                    print(f"Puntos: {puntuacion}")
                    puntaje_antes = db_logic.get_user_score()
                    print(f"Punt antes {puntaje_antes}")
                    db_logic.update_user_score(puntaje_antes + dinero)
                    puntaje_despues = db_logic.get_user_score()
                    print(f"Punt now {puntaje_despues}")
                    # Limpia y cierra Pygame
                    pygame.quit()

                    # Cierra el programa
                    sys.exit()

        ############################# FUNCIONES - DENTRO DE BUCLE #############################
        temporizador()
        FondoMovimiento(fondo)
        
        ############################# BOTONES #############################
        pygame.draw.rect(pantalla,BLANCO,(70,350,300,100),2)

        ############################# TEXTO #############################
        muestra_texto(pantalla,'JUEGO PAUSADO', NEGRO, 90 ,100,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',50)
        muestra_texto(pantalla,'JUEGO PAUSADO', BLANCO, 90 ,100,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',50)
        
        muestra_texto(pantalla,'PUNTUACION',VERDE3, 450 ,320,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',30)
        muestra_texto(pantalla,'PUNTUACION',VERDE2, 450 ,320,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',30)

        muestra_texto(pantalla,str(puntuacion),VERDE3, 570 ,400,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',30)
        muestra_texto(pantalla,str(puntuacion),VERDE2, 570 ,400,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',30)

        muestra_texto(pantalla,'IR A SPS CLOUD',BLANCO, 105 ,387,'../SPSCloud_app/juegos/flappy_bird/fuentes/Minecraft.ttf',30)

        pygame.display.flip()
        
############################################### ELEGIR DIFICULTAD ###############################################
    elif locate == 3:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos()
                # INSTANCIACIÓN DE MONEDAS SEGÚN LA DIFICULTAD ELEGIDA
                if 300 < mouse_pos[0] <  490 and 245 < mouse_pos[1] < 295:
                    for n in range(0,3): # (0,1) Díficil, (0,2) Normal, (0,3)Fácil -> Define la generación de monedas en cada vuelta.
                        moneda = Monedas()  
                        monedaG.add(moneda) # añadimos al grupo Moneda la clase Monedas
                    locate = 1
                elif 285 < mouse_pos[0] < 505 and 345 < mouse_pos[1] < 395:
                    for n in range(0,2):
                        moneda = Monedas()  
                        monedaG.add(moneda) # añadimos al grupo Moneda la clase Monedas
                    locate = 1
                elif 270 < mouse_pos[0] < 525 and 445 < mouse_pos[1] < 495:
                    for n in range(0,1):
                        moneda = Monedas()  
                        monedaG.add(moneda) # añadimos al grupo Moneda la clase Monedas
                    locate = 1
        
        mouse_pos2 = pygame.mouse.get_pos()

        if 300 < mouse_pos2[0] <  490 and 245 < mouse_pos2[1] < 295:
            col1_birdy = VERDE
        elif 285 < mouse_pos2[0] < 505 and 345 < mouse_pos2[1] < 395:
            col3_birdy = NARANJA
        elif 270 < mouse_pos2[0] < 525 and 445 < mouse_pos2[1] < 495:
            col2_birdy = ROJO
        else:
            col1_birdy = BLANCO
            col2_birdy = BLANCO
            col3_birdy = BLANCO

        muestra_texto(pantalla, 'DIFICULTAD', NEGRO, 70, 60, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',65)
        muestra_texto(pantalla, 'DIFICULTAD', BLANCO, 70, 60, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',65)
      
        muestra_texto(pantalla, 'FACIL', NEGRO, 305, 250, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',35)
        muestra_texto(pantalla, 'FACIL', col1_birdy, 305, 250, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',35)

        muestra_texto(pantalla, 'NORMAL', NEGRO, 290, 350, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',35)
        muestra_texto(pantalla, 'NORMAL', col3_birdy, 290, 350, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',35)

        muestra_texto(pantalla, 'DIFICIL', NEGRO, 275, 450, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',35)
        muestra_texto(pantalla, 'DIFICIL', col2_birdy, 275, 450, '../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',35)
      
        temporizador()

        pygame.display.flip()
        FondoMovimiento(fondo)
pygame.quit()