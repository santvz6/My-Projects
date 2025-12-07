# EMPEZADO EN OCUTBRE

from typing import Any
import pygame, random, sys,time
from pygame.locals import *
from pygame.sprite import Group

# PANTALLA
ANCHO = 800
ALTO = 600

# FPS
FPS = 60

# COLORES
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
VERDE= (0,255,0)
VERDE_O1 = (0,102,0)
VERDE_O2 = (0,55,0)
AZUL = (0,0,255)
GRIS = (122,122,122)

# VARIABLES GLOBALES
saltar = False
puntuacion = 0 
x = 0  # FONDO MOVIMIENTO
juego_pausado = False # MENU PAUSA
locate = 0 #0:JUEGO, 1:MENU PAUSA, 2:UA CLOUD

conteo_musica = 0 

conteo = 0
animacion_segundos = 0.1

conteo_2 = 0
animacion_segundos_2 = 0.05

conteo_habilidad = 0
habilidad_segundos = 3

conteo_extra = 0
puntuacion_extra = 0

conteo_2segundos = 0
reinicio_textoflotante = 0
texto_flotante = ''
cooldown_habilidad = 3
tipo_habilidad = -1


# INICIADOR
pygame.init()

# AJUSTES PANTALLA
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Birdy_Sword")
clock = pygame.time.Clock()

# SPRITES SHEETS

moneda_animada = [pygame.image.load('escenario/obstaculos/monedas/m1.png').convert(),
                  pygame.image.load('escenario/obstaculos/monedas/m2.png').convert(),
                  pygame.image.load('escenario/obstaculos/monedas/m3.png').convert(),
                  pygame.image.load('escenario/obstaculos/monedas/m4.png').convert(),
                  pygame.image.load('escenario/obstaculos/monedas/m5.png').convert(),
                  pygame.image.load('escenario/obstaculos/monedas/m6.png').convert()]

espada_animada = [pygame.image.load('escenario/obstaculos/espadas/e1.png').convert_alpha(),
                  pygame.image.load('escenario/obstaculos/espadas/e2.png').convert_alpha(),
                  pygame.image.load('escenario/obstaculos/espadas/e3.png').convert_alpha(),
                  pygame.image.load('escenario/obstaculos/espadas/e4.png').convert_alpha(),
                  pygame.image.load('escenario/obstaculos/espadas/e5.png').convert_alpha()]

fondo = pygame.image.load('escenario/fondo.png')

pajaro = pygame.image.load('jugador/pajaro.png').convert()
pajaro_animado = pygame.transform.scale(pajaro,(pajaro.get_width()- 71,49))

sp_habilidad = pygame.image.load('escenario/obstaculos/mistery_box/box.png').convert()

canciones = ['musica/dry_hands.mp3',
             'musica/wet_hands.mp3',
             'musica/sweden.mp3',
             'musica/mice_on_venus.mp3']

def reproducir_cancion(cancion):
    pygame.mixer.music.load(cancion) # Cargar la canción seleccionada
    pygame.mixer.music.play() # Reproducir la canción que se cargó

# FUNCIONES 
def FondoMovimiento():
    global x # Dado que si ponemos x=0 y lo usamos en un bucle estaría reiniciando la x todo el rato

    #Fondo en movimiento
    x_relativa = x % fondo.get_rect().width
    pantalla.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < ANCHO:
        pantalla.blit(fondo, (x_relativa, 0))
    x -= 1

def muestra_texto(pantalla, texto, color, x, y, fuente, tamaño_letra):
    fuente = pygame.font.Font(fuente,tamaño_letra)
    superficie = fuente.render(texto, True, color) # Texto, Antialiasing, color
    pantalla.blit(superficie, (x, y))

def temporizador():
    global conteo,conteo_2,conteo_extra, conteo_2segundos, reinicio_textoflotante
    global animacion_segundos, animacion_segundos_2
    # tienen que estar fuera para que no los actualice a 0 en el bucle

    tiempo_transcurrido = pygame.time.get_ticks() # 1000 ticks = 1 segundo
    if tiempo_transcurrido > (conteo+1)*(animacion_segundos * 1000):
        conteo +=1
        conteo_extra +=1

    if tiempo_transcurrido > (conteo_2+1)*(animacion_segundos_2 * 1000):
        conteo_2 +=1

    if tiempo_transcurrido > (conteo_2segundos+1)*(2000):
        conteo_2segundos +=1
        reinicio_textoflotante += 1
        
# EJECUCIÓN DE FUNCIONES FUERA DEL BUCLE
reproducir_cancion(canciones[conteo_musica]) # conteo_musica se va modificando dentro del bucle del juego

# CREACIÓN DE CLASES -> Nos ayuda a modificar cada Objeto en particular.
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert(),(70,49))
        self.image.blit(pajaro_animado,(0,0),pygame.Rect(conteo%3 * 69, 0, 70, 49))

        #self.image = pygame.Surface((50,50))
        #self.image.fill(VERDE)
        
        self.rect = self.image.get_rect() # Asignamos a rect el rectángulo del Surface/Imagen
        self.rect.center = (ANCHO // 3, ALTO // 2) # Posición Inicial

        #self.image.fill(ROJO) # Visuaizar la Hitbox

        self.velocidad_y = 0
        self.saltando = False

    def update(self):
    # SE EJECUTA CADA VUELTA DEL BUCLE    

        global saltar # Dado que no quiero usar 'pygame.key.get_pressed()' -> Uso pygame.event y pygame.key en el bucle del juego.
   
        if saltar: 
            self.velocidad_y = -10  # Establece la velocidad hacia arriba
            saltar = False  # Restablece el salto
            

        self.velocidad_y += 0.5 # Aceleración -> Asignamos a la velocidad un aumento 
        self.rect.y += self.velocidad_y # Asignamos a la posición la velocidad

        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert(),(70,49))
        self.image.blit(pajaro_animado,(0,0),pygame.Rect(conteo%3 * 70, 0, 70, 49))
        self.image.set_colorkey(VERDE)
        # MÁRGENES
        if self.rect.y < 0 - self.rect.height: 
            self.rect.y = ALTO

        if self.rect.y > ALTO:
            self.rect.y = 0 - self.rect.height/2 
            self.velocidad_y -= 10
 
class Espadas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(espada_animada[conteo_2%5],(60,30))
        self.image.set_colorkey(VERDE)

        #self.image.fill(ROJO) # Visualizar Hitbox

        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

        self.velocidad_x = 9 # Velocidad inicial

    def update(self):

        self.velocidad_x = 9
        self.rect.x -= self.velocidad_x

        self.image = pygame.transform.scale(espada_animada[conteo_2%5],(60,30))
        self.image.set_colorkey(VERDE)

        if self.rect.x < 0:
            self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

class Monedas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(moneda_animada[conteo % 6],(40,40)) 
        self.image.set_colorkey(AZUL)

        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(ANCHO, ANCHO+100), random.randint(0, ALTO - self.rect.height))

        self.velocidad_x = 0 # Velocidad inicial

    def update(self):
        self.velocidad_x = 10
        self.rect.x -= self.velocidad_x
        self.image = pygame.transform.scale(moneda_animada[conteo%6],(40,40))
        self.image.set_colorkey(AZUL) 
   
        if self.rect.x < 0:
            self.rect.topleft = (random.randint(ANCHO, ANCHO + 100), random.randint(0, ALTO-self.rect.height))

class Habilidad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert(),(70,64))
        self.image.blit(sp_habilidad,(0,0),pygame.Rect(conteo%8 * 68, 0, 70, 64))
        # SPRITE EN MOVIMIENTO - OPTIMIZACIÓN DE SPRITES
        # Tamaño sprite 543 x 64. Conteo suma 1 cada 0.1 segundos. conteo %8: Cada 0.8 segundos movemos la 'x' 68 pixeles
        # ,0 : posición de la y fija en 0. Tamaño del Rect: (70,64)


        self.image.set_colorkey(VERDE)
        #self.image.set_colorkey()

        self.rect = self.image.get_rect()
        self.rect.topleft = (9000, random.randint(0, ALTO - 64))
        #Si va a 10 px por tick = 600px por segundo. Quiero que pase cada 15seg * 600px
 
        self.velocidad_x = 0

    def update(self):

        self.velocidad_x = 10
        self.rect.x -= self.velocidad_x

        self.image.blit(sp_habilidad,(0,0),pygame.Rect(conteo%8 * 68, 0, 70, 64))
        self.image.set_colorkey(VERDE)       

        if self.rect.x < 0 - self.rect.width:
            self.rect.topleft = (9000, random.randint(0, ALTO - 64))
        # Para optimizar y no crear una función de temporizador hacemos que tarde más en reaparecer.



# GRUPOS -> al añadir un grupo se añade un update
playerG = pygame.sprite.Group()
obstaculoG = pygame.sprite.Group()
monedaG = pygame.sprite.Group()
monedaG_habilidad = pygame.sprite.Group() # Grupo para las monedas generadas por la habilidad
habilidadG = pygame.sprite.Group()

# INSTANCIAR OBJETO X
jugador = Jugador()
playerG.add(jugador) # añadimos al Grupo player la clase Jugador()

for n in range(0,6):
    espada = Espadas()
    obstaculoG.add(espada) # añadimos al Grupo obstaculo la clase Espadas()

for n in range(0,3): # (0,1) Díficil, (0,2) Normal, (0,3)Fácil -> Define la generación de monedas en cada vuelta.
    moneda = Monedas()  
    monedaG.add(moneda) # añadimos al grupo Moneda la clase Monedas

habilidad =  Habilidad()
habilidadG.add(habilidad) # añadimos al grupo Habilidad la clase Habilidad()


# BUCLE DEL JUEGO PRINCIPAL
ejecutando = True
while ejecutando:
    if locate == 0: # locate nos ayuda a situarnos, en este caso 0 = juego
        clock.tick(FPS) # Velocidad del bucle de juego, en este caso 60 ticks cada vuelta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False  # Para el bucle del juego si presionamos la 'x' de la ventana.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Si se presiona (KEYDOWN) -> acción deseada
                    saltar = True               
                if event.key == pygame.K_ESCAPE: # Si presionamos ESC -> locate nos lleva al menú de pausa
                    locate = 1
                    
        
        # MÚSICA -> CAMBIO AUTOMÁTICO
        if not pygame.mixer.music.get_busy():   # Reproduciendo canción = True / No reproduciendo = False
            if conteo_musica >= len(canciones)-1:   # Si superamos la longitud de la lista se reproduce la primera canción
                conteo_musica = 0
                reproducir_cancion(canciones[conteo_musica])
            else:   # Al no ser el final, pasamos a la siguiente canción
                conteo_musica += 1
                reproducir_cancion(canciones[conteo_musica])

        
        # ASIGNACIÓN DE TECLAS - MÚSICA
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

        
        # COLISIONES

        # Colisión -> clase - grupo -> Clase:Jugador - Grupo: Obstaculo
        colision_jugador = pygame.sprite.spritecollide(jugador, obstaculoG, True)   #True hace kill() a la clase cuando colisiona
        if colision_jugador:
            puntuacion -= 1
            espada = Espadas()  # Como se elimina al colisionar, instanciamos otra espada
            obstaculoG.add(espada)

        colision_monedas = pygame.sprite.spritecollide(jugador, monedaG, True)
        if colision_monedas:
            puntuacion += 1
            moneda = Monedas()
            monedaG.add(moneda)

        colision_habilidad = pygame.sprite.spritecollide(jugador, habilidadG, True)

        # Necesitamos separar las monedas de las monedas generadas por la habilidad
        colision_habilidad_monedas = pygame.sprite.spritecollide(jugador, monedaG_habilidad, True) 
        #Eliminamos y no generamos las monedas generadas por la habilidad (MONEDAS NO INFINITAS)
        
        if colision_habilidad_monedas:
            puntuacion += 1 # Estas monedas siguen sumando 1

        # Colisión de habilidad / Instanciación de nueva habilidad e Instanciación de lo que hace la habilidad
        if colision_habilidad:
            habilidad = Habilidad()
            habilidadG.add(habilidad)
            tipo_habilidad = random.randint(0,2) # Tipo de habilidad generada aleatoriamente
             
            if tipo_habilidad == 0:     # GENERACIÓN MONEDAS ALEATORIAS
                for n in range(random.randint(0,10)): # Instanciamos 0 o 10 monedas en el grupo dedicado a esta habilidad
                    moneda = Monedas()
                    monedaG_habilidad.add(moneda)   #Grupo dedicado -> monedaG_habilidad -> No se instancia en ningún sitio más
            
            if tipo_habilidad == 1:     # SUMA DE PUNTOS ALEATORIA
                reinicio_textoflotante = 0  # Este reseteo nos servirá para establecer el contador a 0 más adelante
                suma_resta = random.randint(1,10)   # Cantidad aleatoria que se le añadirá a la puntuación
                puntuacion += suma_resta
            elif tipo_habilidad == 2:   #  RESTA DE PUNTOS ALEATORIA
                reinicio_textoflotante = 0
                añadir = random.randint(1,10)
                puntuacion -= suma_resta

        if tipo_habilidad == 1:     # Lo metemos dentro del bucle, no como justo arriba que solo se ejecuta al colisionar.
                                    # Es una gran diferencia que nos ayudará a controlar los temporizadores.
            if reinicio_textoflotante == 1 or reinicio_textoflotante == 0: # reinicio_textoflotante suma 1 cada 2 segundos (VER def temporizador())
                                                                           # por tanto este if se ejecutaría durante 4 segundos
                texto_flotante = str(suma_resta)    # suma_resta -> cantidad aleatoria que se suma
            else:
                texto_flotante = ''     # Cuando pasan los 4 segundos, el texto se mostrará invisible

            muestra_texto(pantalla,texto_flotante,NEGRO, jugador.rect.x + 10 ,jugador.rect.y - 40,'fuentes/m04.TTF',30)
            muestra_texto(pantalla,texto_flotante,VERDE,jugador.rect.x + 10 ,jugador.rect.y - 40,'fuentes/m04b.TTF',30)


        if tipo_habilidad == 2:
            if reinicio_textoflotante == 0 or reinicio_textoflotante == 1:
                texto_flotante = '-' + str(añadir) # suma_resta -> cantidad aleatoria que se resta
            else:
                texto_flotante = ''

            muestra_texto(pantalla,texto_flotante,NEGRO, jugador.rect.x-10 ,jugador.rect.y - 40,'fuentes/m04.TTF',30)
            muestra_texto(pantalla,texto_flotante,ROJO,jugador.rect.x-10 ,jugador.rect.y - 40,'fuentes/m04b.TTF',30)

        # ACTUALIZACIÓN GROUPS
        playerG.update()
        obstaculoG.update()
        monedaG.update()
        monedaG_habilidad.update()
        habilidadG.update()

        # DIBUJO DE SPRITES / TEXTOS / FIGURAS
    
        # pantalla.blit(pygame.image.load('escenario/fondo.png'),(0,0)) -> Fondo estático
        playerG.draw(pantalla)
        obstaculoG.draw(pantalla)
        monedaG.draw(pantalla)
        monedaG_habilidad.draw(pantalla)
        habilidadG.draw(pantalla)

        muestra_texto(pantalla,str(puntuacion),VERDE_O2,47,ALTO-80,'fuentes/Minecraft.ttf',70)
        muestra_texto(pantalla,str(puntuacion),BLANCO,40,ALTO-80, 'fuentes/Minecraft.ttf',70)
        muestra_texto(pantalla,str(round(pygame.mixer.music.get_volume(),2)),BLANCO,750,560,'fuentes/Minecraft.ttf',18)
        muestra_texto(pantalla,'9: BAJAR VOLUMEN',BLANCO,600,550,'fuentes/Minecraft.ttf',13)
        muestra_texto(pantalla,'0: SUBIR VOLUMEN',BLANCO,600,570,'fuentes/Minecraft.ttf',13)
        muestra_texto(pantalla, str(conteo/10),NEGRO,360,15,'fuentes/m04.TTF',30)
        muestra_texto(pantalla, str(conteo/10),BLANCO,360,15,'fuentes/m04b.TTF',30)
        
        # LLAMADA DE FUNCIONES
        temporizador()
         # Actualiza el contenido de la pantalla.
        pygame.display.flip()

        FondoMovimiento() # El fondo tiene que estar situado de esta forma porque sino se superpone a todos los sprites del juego.


        
    
    # MENU DE PAUSA
    
    elif locate==1:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # Al presionar el ESC locate = 0 -> Volver al juego
                    locate = 0 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: # event.button == 1 : Click derecho
                mouse_pos = pygame.mouse.get_pos()
                if 69 < mouse_pos[0] < 371 and 349 < mouse_pos[1] < 451: # Coordenadas del cuadrado que dibujamos más adelante
                    locate = 2  #Nos devuelve al menú de SPS Cloud

        # FUNCIONES
        temporizador()
        FondoMovimiento()
        
        # BOTONES 
        pygame.draw.rect(pantalla,BLANCO,(70,350,300,100),2)

        # TEXTO
        muestra_texto(pantalla,'JUEGO PAUSADO', NEGRO, 90 ,100,'fuentes/m04.TTF',50)
        muestra_texto(pantalla,'JUEGO PAUSADO', BLANCO, 90 ,100,'fuentes/m04b.TTF',50)
        
        muestra_texto(pantalla,'PUNTUACION',VERDE_O2, 450 ,320,'fuentes/m04.TTF',30)
        muestra_texto(pantalla,'PUNTUACION',VERDE_O1, 450 ,320,'fuentes/m04b.TTF',30)

        muestra_texto(pantalla,str(puntuacion),VERDE_O2, 570 ,400,'fuentes/m04.TTF',30)
        muestra_texto(pantalla,str(puntuacion),VERDE_O1, 570 ,400,'fuentes/m04b.TTF',30)

        muestra_texto(pantalla,'IR A SPS CLOUD',BLANCO, 105 ,387,'fuentes/Minecraft.ttf',30)
        
        pygame.display.flip()
        

    elif locate == 2:           # MENU SPS CLOUD
        clock.tick(FPS) 
        for event in pygame.event.get():
            # Se cierra y termina el bucle
            if event.type == pygame.QUIT:
                ejecutando = False

    elif locate == 3:
        print('Juego 2')

pygame.quit()