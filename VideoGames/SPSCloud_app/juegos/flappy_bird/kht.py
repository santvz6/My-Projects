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
locate = 3  #0:SPS CLOUD, 1:BIRDY SWORD, 3:SPS HOOT, 5:SPS CLICK
#####################################################################

#############################################################################
#                               VARIABLES GLOBALES                          #
#############################################################################

######################################## MENÚ BIRDY SWORD ########################################
col1_birdy = BLANCO
col2_birdy = BLANCO
bot_esp1 = 0
bot_esp2 = 0

######################################## BIRDY SWORD ########################################
saltar = False
puntuacion = 0 
dificultad_birdy = 1 # 3 FÁCIL, 2 NORMAL, 1 DIFÍCIL

x = 0  # FONDO MOVIMIENTO

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

######################################## SPSHOOT ########################################
score = 0 # puntuación
loc_preguntas = 1 # locate de primera pregunta

conteo_1segundos = 0 # conteo cada segundo
conteo_animar = 0 # hace de conteo_extra en el otro.

yo = 600 # coordenadas para el movimiento del menú
xo = yo * (8/6) # mantenemos la proporción de 800px / 600px

######################################## JITTER CLCIK ########################################
score_click = 0 # puntuación
rgb = 0 # para añadir textos/colores multicolores

######################################## DUNGEONS ########################################
texto_inicio = 'FILAS'
desplazamiento = 0 # nos servirá cuando texto_incio = 'COLUMNAS'

elegir = 0 # define si elige FILAS o COLUMNAS

filas = 0 # cuántas filas jugará
columnas = 0 # cuántas columnas jugará

tamaño_mapa = [] # uso en funciones -> tomará los valores de [filas,columnas]
ver_mapa = 1 # impar -> mapa invisible, par -> mapa visible

mirando = 'norte' # definimos para donde está mirando el jugador
mirando_conf = False # pos_obj[5]. False -> mirando hacia una pared, True -> puede moverse a donde indique

##### CAMBIO DE COLORES #####
color_puerta = rojo_t # (...)_t -> indica transparencia

flecha_izq = gris_t
flecha_der = gris_t
flecha_atr = gris_t
puerta_del = gris_t

flecha_izq_visible = True
flecha_der_visible = True
flecha_atr_visible = True # SIEMPRE SE PODRÁ IR HACIA ATRÁS -> SIEMPRE SERÁ TRUE
puerta_del_visible = True

movimiento = 0 # define el tipo de movimiento del jugador -> N/S/E/O
jdung_tipo = 0 # define el elemento de la lista de sprites del jugador

##### TAMAÑOS SPRITES #####
tam_jugx = 120 * 2
tam_jugy = 60 * 2
tam_enemx = 549 * 2
tam_enemy = 60 * 2

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

logoi = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/spshoot/SPSLogo.png').convert_alpha()
logo = pygame.transform.scale(logoi,(200,200))

menu = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/spshoot/menu.png').convert_alpha()
espacio = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/spshoot/espacio.png').convert()
planetas = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/spshoot/planeta.png').convert_alpha()

mapa5x5 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/baldosas 5x5.png').convert()
mapa5x7 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/baldosas 5x7.png').convert()
mapa7x5 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/baldosas 7x5.png').convert()
mapa7x7 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/baldosas 7x7.png').convert()
menu_dungeon = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/menu_dungeon.png').convert()

jugador_dung = [pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/JF.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/JE.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/JD.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/JI.png').convert_alpha(),(tam_jugx,tam_jugy))]

enemigo_dung = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/ED.png').convert_alpha(),(tam_enemx,tam_enemy))

mapa_dungeon = [pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/c0.png').convert(),
                pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/c1.png').convert(),
                pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/c2.png').convert(),
                pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/c3.png').convert(),
                pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/c4.png').convert()]
                
ed1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/ed1.png').convert()
ed2 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/ed2.png').convert()
ei1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/ei1.png').convert()
ei2 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/ei2.png').convert()

pi1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/pi1.png').convert()
pd1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/pd1.png').convert()
pa1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/pa1.png').convert()
pb1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/pb1.png').convert()

s1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/s1.png').convert()

pdf1 = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/mazmorras/pdf1.png').convert()

good_ending = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/good_ending.png').convert()
bad_ending = pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/bad_ending.png').convert()

random_dung = random.randint(0,len(mapa_dungeon)-1)
mazmorra = mapa_dungeon[random_dung]

dung_final = good_ending

############################# CARGA DE CANCIONES #############################
canciones = ['../SPSCloud_app/juegos/flappy_bird/musica/dry_hands.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/wet_hands.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/sweden.mp3',
             '../SPSCloud_app/juegos/flappy_bird/musica/mice_on_venus.mp3']

############################# CREACIÓN DE DICCIONARIOS #############################
preguntas = {
    1 : ['¿Cual fue el primer videojuego', 'comercialmente exitoso?'],
    2 : ['¿Cual es el videojuego mas', 'vendido de todos los tiempos?'],
    3 : ['¿Cual es el personaje mas', 'iconico de los videojuegos?'],
    4 : ['¿Cual de los siguientes juegos', 'es un Battle Royale'],
    5 : ['¿Que es un "easter egg" en', 'el contexto de los videojuegos?'],
    6 : ['¿Que es un FPS?',''],
    7 : ['¿Que material es mas','importante en minecraft?'],
    8 : ['¿Quien es CJ?',''],
    9 : ['¿Que es la trifuerza?','']}
respuestas = {
    1 : {'O' : ['Tetris', 'Pong', 'Donkey Kong','Pac-Man'],
         'S' : 'Tetris'},
    2 : {'O' : ['Minecraft', 'GTAV', 'Tetris','Wii Sports'],
         'S' : 'Minecraft'},
    3 : {'O' : ['Mario', 'Sonic', 'Steve','Pac-Man'],
         'S' : 'Mario'},
    4 : {'O' : ['Apex', 'Overwatch', 'COD Ghost','TheWitcher'],
         'S' : 'Apex'},
    5 : {'O' : ['Secreto escondido', 'Huevo misterioso', 'Objeto de pascua','Videojuego'],
         'S' : 'Secreto escondido'}, 
    6 : {'O' : ['FirstPersonShooter', 'FramesPerSecond', 'FifaPesGame','Si'],
         'S' : 'FirstPersonShooter'},
    7 : {'O' : ['Madera','Diamante','Netherite','Cuero'],
         'S' : 'Madera'},
    8 : {'O' : ['Carl Johnson', 'Connor James', 'Cris Johnson', 'Charles James'],
         'S' : 'Carl Johnson'},
    9 : {'O' : ['Reliquia Dorada', 'Fuerza de Hierro', 'Viva SPSCloud', 'Pasapalabra'],
         'S' : 'Reliquia Dorada'}}

for n in range(1,len(respuestas)): # Mezcla/Shuffle las respuestas cuya clave es [n]['O']
    random.shuffle(respuestas[n]['O'])

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

def animar(sprite):
    global xo, yo, conteo_animar
    if conteo_animar == 0:
        xo += 1.001
        yo += 1.001
        sprite_animado = pygame.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
    elif conteo_animar == 1:
        xo -= 1
        yo -= 1
        sprite_animado = pygame.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
    else:
        sprite_animado = pygame.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
        conteo_animar = 0
            
def genPos(mapa):
    global mirando_conf
    centro = [0,0]
###### GENERACIÓN DE POSICIÓN DEL JUGADOR ######
    # DEFINIMOS CENTRO SEGÚN EN TAMAÑO DEL MAPA

    centro[0] = (mapa[0] // 2) + 1 - 1 # EL -1 ME FALTÓ EN EL EXAMEN, SE PONE -1 DEBIDO A QUE TRABAJO CON LISTAS
    centro[1] = (mapa[1] // 2) + 1 - 1
    print(centro)
        
    fila_jug = random.randint(0,mapa[0]-1)    # DEBERIA SER DEL 0 A MAPA - 1 - FALLO EXAMEN
    columna_jug = random.randint(0,mapa[1]-1)
    
    # COMO NO PUEDE SPAWNEAR EN EL CENTRO:
    while fila_jug == centro[0] or columna_jug == centro[1] :
        fila_jug = random.randint(0,mapa[0]-1)
        columna_jug = random.randint(0,mapa[1]-1)
        
###### GENERACIÓN DE POSICIÓN DEL MONSTRUO ######
    fila_mon = random.randint(0,mapa[0]-1)
    columna_mon = random.randint(0,mapa[1]-1)
    
    # COMO NO PUEDE SPAWNEAR EN EL CENTRO:
    while fila_mon == centro[0] or columna_mon == centro[1] or fila_mon == fila_jug or columna_mon == columna_jug:    
        fila_mon = random.randint(0,mapa[0]-1)
        columna_mon = random.randint(0,mapa[1]-1)    
     
    posicion_obj = [centro,fila_jug,columna_jug,fila_mon,columna_mon,mirando_conf]    
    # 0: CENTRO, 1:Xjug, 2:Yjug, 3:Xmon, 4:Ymon
    # 0.0 X, 0.1 Y
    return posicion_obj

def comprobar(pos_obj): # ES NECESARIO QUE SE ESTÉ ACTUALIZANDO LA POS
    global locate, dung_final
    if pos_obj[1] == pos_obj[3] and pos_obj[2] == pos_obj[4]: # SI EL JUGADOR SE ENCUENTRA AL ENEMIGO
        dung_final = bad_ending
        locate = 9
    elif pos_obj[1] == pos_obj[0][0] and pos_obj[2] == pos_obj[0][1]:
        dung_final = good_ending
        locate = 9        
        
def mueve(pos_obj,mapa, movimiento):
    global mirando_conf
     ### EN EL EXAMEN DEFINÍ MAL LAS COORDENADAS PARA DÓNDE SE MUEVE ###
    if movimiento == 1:
        if pos_obj[1] == 0:
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[1] -= 1
            movimiento = 0
            pos_obj[5] = True            
    
    elif movimiento == 3:
        if pos_obj[1] == (mapa[0]-1): #mapa[0] = filas
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[1] += 1
            movimiento = 0
            pos_obj[5] = True
    
    elif movimiento == 2: # este = derecha
        if pos_obj[2] == (mapa[1]-1): #mapa[0] = columnas
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[2] += 1
            movimiento = 0
            pos_obj[5] = True
    elif movimiento == 4:
        if pos_obj[2] == 0:
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[2] -=1
            movimiento = 0
            pos_obj[5] = True

    return pos_obj
  
def change_score():
    pass   

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

class JugDungeon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert_alpha(),(tam_jugy,tam_jugy))
        self.image.blit(jugador_dung[jdung_tipo] ,(40,0),pygame.Rect(conteo_Msegundo%2 * 167, 0, tam_jugx, tam_jugy))


        self.rect = self.image.get_rect() 
        self.rect.center = (0,0) # Posición Inicial del centro del rectángulo obtenido


    def update(self): 
        global movimiento, posicion_act, tamaño_mapa

    
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            if movimiento == 1:
                self.rect.y -= 120
            if movimiento == 2:
                self.rect.x += 120
            if movimiento == 3:
                self.rect.y += 120
            if movimiento == 4:
                self.rect.x -= 120
        

        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert_alpha(),(tam_jugy,tam_jugy)) 
        self.image.blit(jugador_dung[jdung_tipo] ,(40,0),pygame.Rect(conteo_Msegundo%2 * 167, 0, tam_jugx, tam_jugy))
        
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()   
            self.rect.center = (posicion_act[2]*120 + 145, posicion_act[1]*120+60)
        
        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*115 + 40 , posicion_act[1]*115+60)
        
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*86 + 220 , posicion_act[1]*86+25)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*86 + 120 , posicion_act[1]*86+25)

class EnemDungeon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert_alpha(),(tam_enemy,tam_enemy))
        self.image.blit(enemigo_dung ,(-20,0),pygame.Rect(conteo_Msegundo%6 * 192, 0, tam_enemx, tam_enemy))


        self.rect = self.image.get_rect() 
        self.rect.center = (0,0) # Posición Inicial del centro del rectángulo obtenido


    def update(self): 
        global movimiento, posicion_act

        self.image = pygame.transform.scale(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/escenario/prueba.png').convert_alpha(),(tam_enemy,tam_enemy))
        self.image.blit(enemigo_dung ,(-20,0),pygame.Rect(conteo_animacion%6 * 192, 0, tam_enemx, tam_enemy))
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect() 
            self.rect.center = (posicion_act[4]*120+140,posicion_act[3]*120+55) # PROBLEMA: X = COLUMNAS, Y = FILAS

        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect() 
            self.rect.center = (posicion_act[4]*120 + 15,posicion_act[3]*120+55)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[4] * 86 + 220,posicion_act[3]* 83 + 35)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[4] * 86 + 120,posicion_act[3]* 83 + 35)

            
############################# CREACIÓN DE GRUPOS -> al añadir un grupo hay que añadir un update #############################
playerG = pygame.sprite.Group()
obstaculoG = pygame.sprite.Group()
monedaG = pygame.sprite.Group()
monedaG_habilidad = pygame.sprite.Group() # Grupo para las monedas generadas por la habilidad
habilidadG = pygame.sprite.Group()
JugDG = pygame.sprite.Group()
EnemDG = pygame.sprite.Group()


############################# INSTANCIACIÓN DE OBJETOS #############################
jugador = Jugador()
playerG.add(jugador) # añadimos al Grupo player la clase Jugador()

for n in range(0,6):
    espada = Espadas()
    obstaculoG.add(espada) # añadimos al Grupo obstaculo la clase Espadas()

for n in range(0,dificultad_birdy): # Define la generación de monedas según la dificultad seleccionada
    moneda = Monedas()  
    monedaG.add(moneda) # añadimos al grupo Moneda la clase Monedas

habilidad =  Habilidad()
habilidadG.add(habilidad) # añadimos al grupo Habilidad la clase Habilidad()

JD = JugDungeon()
JugDG.add(JD)
ED = EnemDungeon()
EnemDG.add(ED)


ejecutando = True
while ejecutando:
    
############################################################################################################################
#                                                MENU SPS CLOUD                                                            #
############################################################################################################################
    if locate == 0:  
        print(1)  
        clock.tick(FPS) 
        print(2) 
        for event in pygame.event.get():
            print(3) 
            if event.type == pygame.QUIT:
                ejecutando = False
                print(4) 
                
    ############################# CONVERSOR #############################
        print(5) 
        if conversor:
            ##### SPS CLICK #####
            dinero += score_click//10
            score_click = 0
            ##### BIRDY SWORD ######
            dinero += puntuacion
            puntuacion = 0
            ##### SPS HOOT ######
            dinero += score
            score = 0
            print(6) 
            conversor = False
        print(7) 
        

       

    ################ LLAMADA FUNCIONES DENTRO DE BUCLE ################
        temporizador()

############################################################################################################################
#                                                    BIRDY SWORD MENÚ                                                      #
############################################################################################################################
    elif locate == -1:
        clock.tick(FPS) # Velocidad del bucle de juego, en este caso 60 ticks cada vuelta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False  # Finaliza el bucle del juego si presionamos la 'x' de la ventana.

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN

                if 195 < mouse_pos[0] < 375 and 485 < mouse_pos[1] < 540: # Coordenadas del BOTÓN PLAY
                    locate = 1
                elif 445 < mouse_pos2[0] < 635 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN SALIR
                    locate = 0

        mouse_pos2 = pygame.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN

        if 195 < mouse_pos2[0] < 375 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN JUGAR
            col1_birdy = VERDE # Animación de color / Botón jugar
            bot_esp1 += 0.2 # Animación espada
        elif 445 < mouse_pos2[0] < 635 and 485 < mouse_pos2[1] < 540: # Coordenadas del BOTÓN SALIR
            col2_birdy = ROJO
            bot_esp2 += 0.2
        else: # Volver a establecer valores por defecto
            bot_esp1 = 0
            bot_esp2 = 0
            col1_birdy = BLANCO
            col2_birdy = BLANCO

        ############### DIBUJO DE SPRITES ###############
        pantalla.blit(pygame.transform.rotate(pygame.transform.scale(espada_animada[int(round(bot_esp1,0))%5],(86.4,42)),220), (172,460))
        pantalla.blit(pygame.transform.rotate(pygame.transform.scale(espada_animada[int(round(bot_esp2,0))%5],(86.4,42)),320), (572,460))

        muestra_texto(pantalla,'JUGAR',NEGRO,200,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',34)
        muestra_texto(pantalla,'JUGAR',col1_birdy,200,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',34)

        muestra_texto(pantalla,'SALIR',NEGRO,450,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04.TTF',34)
        muestra_texto(pantalla,'SALIR',col2_birdy,450,500,'../SPSCloud_app/juegos/flappy_bird/fuentes/m04b.TTF',34)

        ############################# LLAMADA DE FUNCIONES - DENTRO DE BUCLE #############################
        temporizador()
       
        pygame.display.flip()  # Actualiza el contenido de la pantalla.
        FondoMovimiento(menu_birdy) 

############################################################################################################################
#                                                   BIRDY SWORD BUCLE                                                      #
############################################################################################################################

    elif locate == 1: # locate nos ayuda a situarnos, en este caso 0 = BIRDY SWORD
        clock.tick(FPS) # Velocidad del bucle de juego, en este caso 60 ticks cada vuelta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False  # Finaliza el bucle del juego si presionamos la 'x' de la ventana.
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
                if event.key == pygame.K_ESCAPE:    # Al presionar el ESC locate = 0 -> Volver al juego BIRDY SWORD
                    locate = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos()
                if 69 < mouse_pos[0] < 371 and 349 < mouse_pos[1] < 451: # Coordenadas del cuadrado que dibujamos más adelante

                    ##### SPS CLICK #####
                    dinero += score_click//10
                    score_click = 0
                    ##### BIRDY SWORD ######
                    dinero += puntuacion
                    puntuacion = 0
                    ##### SPS HOOT ######
                    dinero += score
                    score = 0
                    print(6) 
                    conversor = False
                    print(f"Dinero: {dinero}")
                    print(f"Puntos: {puntuacion}")
                    puntaje_antes = db_logic.get_user_score()
                    print(f"Punt antes {puntaje_antes}")
                    db_logic.update_user_score(puntaje_antes + dinero)
                    puntaje_despues = db_logic.get_user_score()
                    print(f"Punt now {puntaje_despues}")
                    main_window.ui.label_3.setText(str(puntaje_despues)) # Linea con puntaje del usario
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

############################################################################################################################
#                                                      SPS HOOT                                                            #
############################################################################################################################
    elif locate == 3:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Se cierra y termina el bucle
            if event.type == pygame.QUIT:
                ejecutando = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                    mouse_pos = pygame.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN
                    if 240 < mouse_pos[0] < 560 and 440 < mouse_pos[1] < 540: # Coordenadas del BOTÓN PLAY
                        locate = 4 # Preguntas SPS HOOT
  
        ############### DIBUJO SPRITES - FIGURAS- TEXTOS ###############
        #pygame.draw.rect(pantalla,BLANCO,(240,440,320,100),5) HITBOX BOTÓN PLAY
        pantalla.blit(planetas,(0,0))

        ############### LLAMADA DE FUNCIONES - DENTRO DE BUCLE ###############
        temporizador()
        animar(menu)
        temporizador()
        
        ############### ACTUALIZACIÓN DE LA PANTALLA ###############
        pygame.display.flip()
        pantalla.blit(espacio,(0,0))
        
############################################################################################################################
#                                                    PREGUNTAS SPS HOOT                                                    #
############################################################################################################################
    elif locate == 4:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                    mouse_pos = pygame.mouse.get_pos()

                ################ RECONOCMINETO DE OPCIÓN SELECCIONADA ################

                    # Si la respuesta de la pregunta es igual al primer elemento de la lista de opciones: Rectángulo azul
                    if respuestas[loc_preguntas]['S'] == opciones[0]: # loc_preguntas: Nos sitúa en la pregunta.
                        if 20 < mouse_pos[0] < 400 and 220 < mouse_pos[1] < 400: 
                            score += 1 # Si hace click en el rect correcto se suma 1 ...
                            print(score)
                            loc_preguntas += 1
                        else:
                            loc_preguntas += 1 # ...sino, se pasa a la siguiente pregunta

                    # Si la respuesta de la pregunta es igual al segundo elemento de la lista de opciones: Rectángulo rojo
                    elif respuestas[loc_preguntas]['S'] == opciones[1]:
                        if 400 < mouse_pos[0] < 780 and 220 < mouse_pos[1] < 400:
                            score += 1
                            print(score)
                            loc_preguntas += 1
                        else:
                            loc_preguntas += 1

                    # Si la respuesta de la pregunta es igual al tercer elemento de la lista de opciones: Rectángulo verde
                    elif respuestas[loc_preguntas]['S'] == opciones[2]:
                        if 20 < mouse_pos[0] < 400 and 400 < mouse_pos[1] < 580:
                            score += 1
                            print(score)
                            loc_preguntas += 1
                        else:
                            loc_preguntas += 1

                    # Si la respuesta de la pregunta es igual al cuarto elemento de la lista de opciones: Rectángulo amarillo
                    elif respuestas[loc_preguntas]['S'] == opciones[3]:
                        if 400 < mouse_pos[0] < 780 and 400 < mouse_pos[1] < 580:
                            score += 1
                            print(score)
                            loc_preguntas += 1
                        else:
                            loc_preguntas += 1

################ LOCALIZACIÓN DE PREGUNTAS Y RESPUESTAS ################

        # Al ser un if dentro del While -> While esto se cumpla:
        if loc_preguntas < len(preguntas)+1:
            pregunta = preguntas.get(loc_preguntas) # pregunta toma los elementos del diccionario preguntas por el que el usuario va
            respuesta = respuestas.get(loc_preguntas) # respuesta toma los elementos del diccionario respuestas por el que el usuario va
            
            opciones = respuesta.get('O') # Nos devuelve la lista con los cuatro elementos de la pregunta
            solucion = respuesta.get('S') # Nos devuelve el elemento que es la solución de la pregunta
        
        if loc_preguntas == len(preguntas)+1: # Cuando llegamos al final de las preguntas
            loc_preguntas = 1 # Volvemos a la primera pregunta
            conversor = True
            locate = 0 
            ##### SPS CLICK #####
            dinero += score_click//10
            score_click = 0
            ##### BIRDY SWORD ######
            dinero += puntuacion
            puntuacion = 0
            ##### SPS HOOT ######
            dinero += score
            score = 0
            print(6) 
            conversor = False
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

            
        

################ DIBUJO DE TEXTO, FIGURAS, SPRITES ################

        ########### TÍTULO DE LA PREGUNTA ###########
        muestra_texto(pantalla,pregunta[0], BLANCO, 180, 50, '../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',45)
        muestra_texto(pantalla,pregunta[0], NEGRO, 180, 50, '../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',45)
        muestra_texto(pantalla,pregunta[1], BLANCO, 200, 100, '../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',45)
        muestra_texto(pantalla,pregunta[1], NEGRO, 198.75, 100, '../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',45)

        ########### RECTÁNGULOS DE COLORES ###########    
        pygame.draw.rect(pantalla, AZUL, (20,220,380,180))
        pygame.draw.rect(pantalla, ROJO, (400,220,380,200))
        pygame.draw.rect(pantalla, VERDE, (20,400,380,180))
        pygame.draw.rect(pantalla, AMARILLO, (400,400,380,180))
        
        ########### LÍNEAS DE CONTORNO DE LOS RECTÁNGULOS ###########
        pygame.draw.line(pantalla,NEGRO,(20,220),(780,220),5)
        pygame.draw.line(pantalla,NEGRO,(20,580),(780,580),5)
        pygame.draw.line(pantalla,NEGRO,(20,220),(20,580),5)
        pygame.draw.line(pantalla,NEGRO,(780,220),(780,580),5)

        ########### DIBUJO DE LAS 4 FIGURAS DE COLORES ###########
        pygame.draw.rect(pantalla, AZUL1, (130,240,140,140))
        pygame.draw.rect(pantalla, NEGRO, (130,240,140,140),5)

        pygame.draw.polygon(pantalla, VERDE1, ((100,560),(200,420),(300,560)))
        pygame.draw.polygon(pantalla, NEGRO, ((100,560),(200,420),(300,560)),5)

        pygame.draw.circle(pantalla, ROJO2, (580,310),70)
        pygame.draw.circle(pantalla, NEGRO, (580,310),70,5)

        pygame.draw.polygon(pantalla, AMARILLO1, ((580,420),(660,490),(580,560),(500,490)))
        pygame.draw.polygon(pantalla, NEGRO, ((580,420),(660,490),(580,560),(500,490)),5)

        ########### TEXTO DE LAS SOLUCIONES ###########
        muestra_texto(pantalla, opciones[0], NEGRO, 140,280,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',40)
        muestra_texto(pantalla, opciones[1], NEGRO, 530,280,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',40)
        muestra_texto(pantalla, opciones[2], NEGRO, 150,475,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',40)
        muestra_texto(pantalla, opciones[3], NEGRO, 530,465,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',40)

        muestra_texto(pantalla, opciones[0], BLANCO, 140,280,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',40)
        muestra_texto(pantalla, opciones[1], BLANCO, 530,280,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',40)
        muestra_texto(pantalla, opciones[2], BLANCO, 150,475,'../SPSCloud_app/juegos/flappy_bird/fuentes/Gout.ttf',40)
        muestra_texto(pantalla, opciones[3], BLANCO, 530,465,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',40)

        ########### TEXTO PUNTAJE ###########
        muestra_texto(pantalla,str(score),NEGRO,382,355,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',45)
        muestra_texto(pantalla,str(score),BLANCO,382,355,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',45)

        temporizador()
        pygame.display.flip()
        pantalla.blit(espacio,(0,0))

############################################################################################################################
#                                                    SPS CLICK                                                             #
############################################################################################################################
    elif locate == 5:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos()

                if 50 < mouse_pos[0] < 750 and 200<mouse_pos[1]<550: # RECTÁNGULO DE CLCIK
                    score_click += 1
                    rgb += 11.25

                elif 10< mouse_pos[0]<90 and 15 < mouse_pos[1] < 55: # RECTÁNGULO DE SALIR
                    conversor = True
                    locate = 0

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    score_click += 1
                    rgb += 11.25
                
        rgb = (rgb + 1) % 360
        
        # Convertir el tono a RGB
        color_rgb = pygame.Color(0,0,0,255) # COLOR BASE
        color_rgb.hsva = (rgb,100,100,100) # COLOR, SATURACIÓN, BRILLO, OPACIDAD

        pygame.draw.rect(pantalla,(183,69,206),(50,200,700,350))

        pygame.draw.rect(pantalla,BLANCO,(50,200,700,350),5)
        pygame.draw.rect(pantalla,BLANCO, (0,0,800,600),5)

        muestra_texto(pantalla, str(score_click),color_rgb, 375,330,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',55)
        muestra_texto(pantalla, str(score_click),BLANCO, 375,330,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',55)
        muestra_texto(pantalla, str(score_click),(183,69,206), 371.8,330,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',55)

        muestra_texto(pantalla, 'SPS CLICK',(183,69,206), 275,50,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',65)  
        muestra_texto(pantalla, 'SPS CLICK',color_rgb, 271.8,50,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',65)
        muestra_texto(pantalla, 'SPS CLICK',BLANCO, 275,50,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',65)
          
        muestra_texto(pantalla,'pulsa SPACE',(229,76,224),360,215,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',20)
        muestra_texto(pantalla,'pulsa SPACE',BLANCO,360,215,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',20)

        muestra_texto(pantalla,'haz CLICK',(229,76,224),360,490,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',20)
        muestra_texto(pantalla,'haz CLICK',BLANCO,360,490,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',20)

        muestra_texto(pantalla,'SALIR',(183,69,206),30,20,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSha.ttf',20)
        muestra_texto(pantalla,'SALIR',color_rgb,29.5,20,'../SPSCloud_app/juegos/flappy_bird/fuentes/GOut.ttf',20)
        muestra_texto(pantalla,'SALIR',BLANCO,30,20,'../SPSCloud_app/juegos/flappy_bird/fuentes/GSol.ttf',20)
        
        temporizador() # PARA QUE SE VAYAN EJECUTANDO LOS CONTEOS DEBIDO A LOS TICKS
        pygame.display.flip()
        pantalla.fill((229,76,224))

################################################################################################################
#                                 SPS DUNGEON ------ SELECCIÓN AJUSTES PARTIDA                                 #
################################################################################################################    
    elif locate == 6:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN  and event.button==1: # CLICK IZQUIERDO ->
                mouse_pos = pygame.mouse.get_pos() # Obtener posición del cursor           
                if elegir == 0: # Elegir = 0 -> elegir filas
                    if 140 < mouse_pos[0] < 280 and 0 < mouse_pos[1] < 520: # Si se presiona el polígono izq(5)
                        texto_inicio = 'COLUMNAS'
                        desplazamiento = 35 # Desplazamiento para centrar el nuevo texto 'COLUMNAS'
                        filas = 5 # Establecemos 5 filas
                        elegir += 1 # Elegir = 1 -> elegir columnas

                    elif 540 < mouse_pos[0] < 680 and 0 < mouse_pos[1] < 520:
                        texto_inicio = 'COLUMNAS'
                        desplazamiento = 35
                        filas = 7 # Establecer 7 filas
                        elegir += 1
                    
                elif elegir == 1:
                    if 140 < mouse_pos[0] < 280 and 0 < mouse_pos[1] < 520:
                        #texto_inicio = '' # ¿necesario?
                        desplazamiento = 0 # Reinicio del desplazamiento
                        columnas = 5
                        tamaño_mapa = [filas,columnas] # Establecemos la variable según las dimensiones elegidas para el mapa

                        posicion_objetos = genPos(tamaño_mapa) # generación posiciones iniciales (posicion_objetos)
                        posicion_act = mueve(posicion_objetos,tamaño_mapa,movimiento) # primera actualización de posiciones (posicion_act)

                        if ver_mapa % 2 == 0: # Ver mapa -> define según el usuario elige si se ejecuta ...
                            locate = 7 # ... el juego con opción de visuallizar la posición de jugador y enemigo o ...                        
                        else:
                            locate = 8 # ... el juego sin conocer las posiciones y viendo tan solo mazmorras.

                    elif 540 < mouse_pos[0] < 680 and 0 < mouse_pos[1] < 520:
                        texto_inicio = ''
                        desplazamiento = 0
                        columnas = 7
                        tamaño_mapa = [filas,columnas]

                        posicion_objetos = genPos(tamaño_mapa) # GENERAMOS LAS POSICIONES INICIALES
                        posicion_act = mueve(posicion_objetos,tamaño_mapa,movimiento)
                        
                        if ver_mapa % 2 == 0:
                            locate = 7
                        else:
                            locate = 8

                if 360 < mouse_pos[0] < 450 and 200 < mouse_pos[1] < 330: # Si se hace click en la puerta de (visualizar_mapa)
                    if ver_mapa % 2 == 0:
                        color_puerta = rojo_t # Rojo indica -> no visualizar mapa
                    else:
                        color_puerta = verde_t # Verde -> visualizar mapa
                    ver_mapa += 1 # Dado que trabajamos con números pares o impares (n + 1)
                    print(ver_mapa)

    ############ OBTENEMOS LA POSICIÓN DEL CURSOR EN CADA MOMENTO ############
        mouse_pos2 = pygame.mouse.get_pos()

        ### DETALLE CURSOR SELECCIONANDO FILAS/COLUMNAS, SÍ/NO MOSTRAR MAPA ###
        if 140 < mouse_pos2[0] < 280 and 0 < mouse_pos2[1] < 520:
            pygame.draw.polygon(pantalla, BLANCO, ((140, 0), (140, 520), (280, 385), (280, 80)),5) # Polígono izq (5)
        elif 540 < mouse_pos2[0] < 680 and 0 < mouse_pos2[1] < 520:
            pygame.draw.polygon(pantalla, BLANCO, ((680, 0), (680, 520), (540, 385), (540, 80)),5) # Polígono der (7)      
        elif 360 < mouse_pos2[0] < 450 and 200 < mouse_pos2[1] < 330:
            pygame.draw.rect(pantalla, BLANCO, (360,200,90,130),2) # Puerta (VER MAPA)

        ############### DIBUJO DE FIGURAS Y TEXTOS ###############
        superficie_poligono = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA) # CREAMOS UNA SUPERFICIE CON OPACIDAD (SRCALPHA)
        pygame.draw.polygon(superficie_poligono, azul_t, ((140, 0), (140, 520), (280, 385), (280, 80))) # DIBUJAMOS SOBRE ESTA SUPERFICIE
        pygame.draw.polygon(superficie_poligono, lila_t, ((680, 0), (680, 520), (540, 385), (540, 80)))
        pygame.draw.rect(superficie_poligono, color_puerta, (360,200,90,130))        

        # Usamos 'desplazamiento' porque el texto de columnas es más largo que el de filas -> CENTRAR TEXTO
        muestra_texto(pantalla,str(texto_inicio),NEGRO, 373-desplazamiento,170,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval2.ttf',30) 
        muestra_texto(pantalla,str(texto_inicio),BLANCO, 370-desplazamiento,170,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval2.ttf',30)
        
        muestra_texto(pantalla,'5',BLANCO,200,210,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval.ttf',50)
        muestra_texto(pantalla,'7',BLANCO,600,210,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval.ttf',50)

        temporizador() # Actualiza los sprites sheets de los juegos        
        pygame.display.flip()
        pantalla.blit(menu_dungeon,(0,0))
        pantalla.blit(superficie_poligono, (0, 0)) # AÑADIR A LA PANTALLA LA SUPERFICIE CON OPACIDAD

################################################################################################################
#                                    SPS DUNGEON ------ MODO MAPA VISIBLE                                      #
################################################################################################################
    elif locate == 7:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
        ################ MOVIMIENTO SEGÚN LA TECLA PRESIONADA ################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    movimiento = 4
                    jdung_tipo = 3 # SPRITE PERSONAJE MIRANDO OESTE
                elif event.key == pygame.K_d:
                    movimiento = 2
                    jdung_tipo = 2 # SPRITE PERSONAJE MIRANDO ESTE
                elif event.key == pygame.K_w:
                    movimiento = 1
                    jdung_tipo = 1 # SPRITE PERSONAJE MIRANDO SUR
                elif event.key == pygame.K_s:
                    movimiento = 3
                    jdung_tipo = 0 # SPRITE PERSONAJE MIRANDO NORTE
            
        ################ RETURN DE POSICION ACTUAL DEL JUGADOR EN CADA MOVIMIENTO ################
                posicion_act = mueve(posicion_act,tamaño_mapa,movimiento) # actualiza la posición todo el rato que se mueve
                comprobar(posicion_act)

    ################### CARGA DE FONDO DEPENDIENDO DEL MAPA ELEGIDO ###################    
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            pantalla.blit(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/fb 5x5.png').convert(),(0,0))
            pantalla.blit(mapa5x5,(100,0))
        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            pantalla.blit(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/fb 5x7.png').convert(),(0,0))
            pantalla.blit(mapa5x7,(0,15))
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            pantalla.blit(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/fb 7x5.png').convert(),(13,0))
            pantalla.blit(mapa7x5,(200,0))
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            pantalla.blit(pygame.image.load('../SPSCloud_app/juegos/flappy_bird/dungeon/fb 7x7.png').convert(),(0,0))
            pantalla.blit(mapa7x7,(100,0))
    ###################################################################################

        ### DIBUJO Y ACTUALIZACIÓN DE CLASES ###
        JugDG.update()
        JugDG.draw(pantalla)
        EnemDG.update()
        EnemDG.draw(pantalla)     

        temporizador() # ACTUALIZA LOS SPRITES SHEETS DE TODOS LOS JUEGOS
        pygame.display.flip()        
        #movimiento = 0 # LA FUNCIÓN MUEVE() YA INCLUYE ESTE REINICIO

################################################################################################################
#                                    SPS DUNGEON ------ MODO MAPA INVISIBLE                                      #
################################################################################################################        
    elif locate == 8:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False            
            if event.type == pygame.MOUSEBUTTONDOWN  and event.button==1: # CUANDO SE HACE CLICK IZQUIERDO
                mouse_pos = pygame.mouse.get_pos()

                ######################### MOVIMIENTO - NORTE #########################
                if 372 < mouse_pos2[0] < 425 and 405 < mouse_pos2[1] < 445:
                    if mirando == 'norte':
                        movimiento = 1 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]: # pos_act[5] -> comprueba que el movimiento es válido y no hay ninguna pared (VALOR BOOLEANO)
                            mirando = 'norte' # si no hay pared y se permite (True) -> establece mirando y genera un número aleatorio ...   
                            random_dung = random.randint(0,len(mapa_dungeon)-1) # ... este número establece el fondo de la nueva mazmorra

                    elif mirando == 'este':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)
                    elif mirando == 'sur':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)
                    elif mirando == 'oeste':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)            

                ######################### MOVIMIENTO - ESTE #########################
                elif 598 < mouse_pos2[0] < 660 and 510 < mouse_pos2[1] < 540:          
                    if mirando == 'norte':
                        movimiento = 2 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)                      
                    elif mirando == 'este':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)                      

                ######################### MOVIMIENTO - SUR #########################
                elif 315 < mouse_pos2[0] < 440 and 545 < mouse_pos2[1] < 580:
                    if mirando == 'norte':
                        movimiento = 3 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'este':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  

                ######################### MOVIMIENTO - OESTE #########################
                elif 50 < mouse_pos2[0] < 115 and 475 < mouse_pos2[1] < 505:
                    if mirando == 'norte':
                        movimiento = 4 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'este':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  

################# OBTENER POSICIÓN DEL RATÓN EN CADA MOMENTO #################
        mouse_pos2 = pygame.mouse.get_pos()


##########################################################################################
#          ESTABLECER MAZMORRA Y FLECHAS VISIBLES DEPENDIENDO DE 'MIRANDAO'              #
##########################################################################################
        
        if mirando == 'norte':
            if posicion_act[2] == 0 and posicion_act[1] == 0: # ESQUINA IZQ SUP
                mazmorra = ed2
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == 0: # PASILLO IZQUIERDO
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == 0: #ESQUINA DER SUP
                mazmorra = ei1
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[1] == 0:
                mazmorra = pa1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] and posicion_act[1] == posicion_act[0][1] + 1 :
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True

        elif mirando == 'sur':
            if posicion_act[2] == 0 and posicion_act[1] == tamaño_mapa[1] - 1: # ESQUINA IZQ INF
                mazmorra = ei1
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == 0: #PASILLO IZQUIERDO
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == tamaño_mapa[1] - 1: #ESQUINA DER INF
                mazmorra = ed1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pb1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] and posicion_act[1] == posicion_act[0][1] - 1:
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
        
        elif mirando == 'este':
            if posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == 0: #ESQUINA DER SUP
                mazmorra = ed2
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == tamaño_mapa[1] - 1: #ESQUINA DER INF
                mazmorra = ei2
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pdf1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[1] == 0: # PASILLO SUPERIOR
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] - 1 and posicion_act[1] == posicion_act[0][1]: #PUERTA
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            
        elif mirando == 'oeste':
            if posicion_act[2] == 0 and posicion_act[1] == 0: # ESQUINA IZQ SUP
                mazmorra = ei2
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == 0 and posicion_act[1] == tamaño_mapa[1] - 1: # ESQUINA IZQ INF
                mazmorra = ed1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == 0: #PASILLO IZQUIERDO
                mazmorra = pdf1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[1] == 0: # PASILLO SUPERIOR
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == posicion_act[0][0] + 1 and posicion_act[1] == posicion_act[0][1]:
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True

###################################################################################################################
#                                    CONFIGURACION DE COLORES DE FLECHAS                                          #
###################################################################################################################

        ################### RATÓN EN FLECHA DELANTERA ###################
        if 372 < mouse_pos2[0] < 425 and 405 < mouse_pos2[1] < 445:
            if puerta_del_visible:
                puerta_del = BLANCO # Si el ratón está en la flecha delantera y esta es visible, colorear de BLANCO
        else:
            if puerta_del_visible: # Si es visible pero el ratón no está en la flecha, colorear de gris_t
                puerta_del = gris_t    
        ################### RATÓN EN FLECHA IZQUIERDA ###################
        if 50 < mouse_pos2[0] < 115 and 475 < mouse_pos2[1] < 505: 
            if flecha_izq_visible:
                flecha_izq = BLANCO
        else:
            if flecha_izq_visible:
                flecha_izq = gris_t
        ################### RATÓN EN FLECHA DERECHA ###################
        if 598 < mouse_pos2[0] < 660 and 510 < mouse_pos2[1] < 540: 
            if flecha_der_visible:
                flecha_der = BLANCO
        else:
            if flecha_der_visible:
                flecha_der = gris_t
        ################### RATÓN EN FLECHA TRASERA ###################
        if 315 < mouse_pos2[0] < 440 and 545 < mouse_pos2[1] < 580: 
            flecha_atr = BLANCO
        else:
            flecha_atr = gris_t # No necesita else, siempre está visible

        ################### FLECHA NO VISIBLE = NO MOSTRAR (colorear de trans) ###################
        if not flecha_izq_visible:
            flecha_izq = trans
        if not flecha_der_visible:
            flecha_der = trans
        if not puerta_del_visible:
            puerta_del = trans

#################################################################################################
#                         FIN COORDENADAS Y FLECHAS DEL MODO MAZMORRAS                          #
#                                                                                               #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
#                                DIBUJO DE FLECHAS Y MÁS FIGURAS                                #
#################################################################################################

        superficie_poligono = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA) # SUPERFICIE CON TRANSPARENCIA
        
        #### DIBUJO DE FLECHS ####
        muestra_texto(superficie_poligono, 'Volver atras',flecha_atr,320,550,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval2.ttf', 30 )
        pygame.draw.polygon(superficie_poligono, flecha_izq, ((50,490), (93,477), (77,489),(114,489),(108,495),(73,495),(60,505)))
        pygame.draw.polygon(superficie_poligono, flecha_der,  ((596,522),(628,522),(620,510),(658,523),(638,539),(630,529),(600,528)))
        pygame.draw.polygon(superficie_poligono, puerta_del,  ((410,405),(425,420),(410,420),(396,445),(372,445),(389,420),(373,420)))

        ### DIBUJO Y ACTUALIZACIÓN DE CLASES ###
        JugDG.update()
        JugDG.draw(pantalla)
        EnemDG.update()
        EnemDG.draw(pantalla) 

        pygame.display.flip() # ACTUALIZACIÓN DE PANTALLA
        
        pantalla.blit(mazmorra,(0,0)) # MOSTRAMOS EL FONDO ...
        pantalla.blit(superficie_poligono, (0, 0)) # ... Y ENCIMA LA SUPERFICIE TRANSPARENTE

###################################################################################################################
#                                  FIN DE PARTIDA - VOLVER A JUGAR / SALIR                                        #
###################################################################################################################
    elif locate == 9:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN  and event.button==1:
                mouse_pos = pygame.mouse.get_pos()
                if 200 < mouse_pos2[0] < 350 and 280 < mouse_pos2[1] < 350: #BOTÓN JUGAR
                    locate = 6 # VOLVER A LA CONFIGURACIÓN DE LA PARTIDA
                    elegir = 0
                    filas = 0
                    columnas = 0
                    texto_inicio = 'FILAS'
                    jdung_tipo = 0
                elif 450 < mouse_pos2[0] < 600 and 280 < mouse_pos2[1] < 350: #BOTÓN SALIR
                    locate = 0 # VOLVER AL MENÚ SPS CLOUD
                    elegir = 0
                    filas = 0
                    columnas = 0
                    texto_inicio = 'FILAS'
                    jdung_tipo = 0

        superficie_poligono = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA) # SUPERFICIE CON TRANSPARENCIA

        puerta_del = gris_t # Tiene que ir antes del if // Uso 'puerta_del' para reutilizar variables...
        flecha_atr = gris_t # ...debido a que puerta_del' no se está usando.
        flecha_der = gris_t
        flecha_izq = gris_t
        
        mouse_pos2 = pygame.mouse.get_pos()

        if 200 < mouse_pos2[0] < 350 and 280 < mouse_pos2[1] < 350: # BOTÓN JUGAR
            puerta_del = BLANCO
            flecha_atr = AMARILLO
        if 450 < mouse_pos2[0] < 600 and 280 < mouse_pos2[1] < 350: #BOTOÓN SALIR
            flecha_izq = BLANCO
            flecha_der = BLANCO
           
        pygame.draw.rect(superficie_poligono,puerta_del,(200,280,150,70),1) # BOTÓN JUGAR        
        muestra_texto(superficie_poligono,'JUGAR',flecha_atr,226,302,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval2.ttf',35)

        muestra_texto(superficie_poligono,'SALIR',flecha_der,480,302,'../SPSCloud_app/juegos/flappy_bird/fuentes/medieval2.ttf',33) # BOTÓN SALIR
        pygame.draw.rect(superficie_poligono,flecha_izq,(450,280,150,70),1)

        pygame.display.flip()
        pantalla.blit(dung_final,(0,0))
        pantalla.blit(superficie_poligono,(0,0))

pygame.quit()