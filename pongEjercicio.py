from random import randint 
import pygame 

ALTO = 600
ANCHO = 800
ALTO_PALA = 100
ANCHO_PALA = 20
MARGEN = 30

COLOR_FONDO = (0, 0, 0)  
COLOR_OBJETOS = (200, 200, 200) 
COLOR_LETRAS = (0, 200, 0)
COLOR_RED = (50,50,50)

VEL_JUGADOR = 10   
FPS = 60 
VEL_PELOTA = 10 

TAM_LETRA_MARCADOR = 150
TAM_LETRA_MENSAJE = 40

class Pintable(pygame.Rect):

    def pintame(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_OBJETOS, self)


class Pelota(Pintable): 

    tam_pelota = 10

    def __init__(self):
        
        super().__init__(
            (ANCHO - self.tam_pelota)/2, 
            (ALTO-self.tam_pelota)/2,
            self.tam_pelota,
            self.tam_pelota)
        
        self.vel_y = randint(-VEL_PELOTA, VEL_PELOTA) 
        self.vel_x = 0
        while self.vel_x == 0: 
            self.vel_x = randint(-VEL_PELOTA, VEL_PELOTA)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y <= 0:
            self.vel_y = -self.vel_y
        if self.y >= (ALTO-self.tam_pelota):
            self.vel_y = -self.vel_y

        if self.x <= 0:
            self.reiniciar(True)
            return 2
        if self.x >= (ANCHO - self.tam_pelota):
            self.reiniciar(False)
            return 1
        return 0


    def reiniciar(self, haciaIzquierda):
        self.x = (ANCHO - self.tam_pelota)/2
        self.y = (ALTO-self.tam_pelota)/2
        self.vel_y = randint(-VEL_PELOTA, VEL_PELOTA)
        if haciaIzquierda:
            self.vel_x = randint(-VEL_PELOTA, -1)
        else:
            self.vel_x = randint(1, VEL_PELOTA)


class Jugador(Pintable):

    def __init__(self, x):
        arriba = (ALTO-ALTO_PALA) / 2    
        super().__init__(x, arriba, ANCHO_PALA, ALTO_PALA) 

    def subir(self): 
        posicion_minima = 0
        self.y -= VEL_JUGADOR
        if self.y < posicion_minima:
            self.y = posicion_minima

    def bajar(self): 
        posicion_maxima = ALTO - ALTO_PALA
        self.y += VEL_JUGADOR
        if self.y > posicion_maxima:
            self.y = posicion_maxima

class Mensaje:

# Creo mensaje como clase para aprovechar el método "preparar_tipografia"; en un futuro podría ser útil (si quisiera, por ejemplo, crear un menú de pausa)

    def preparar_tipografia(self, tam_letra):
        tipos = pygame.font.get_fonts()
        letra = 'comicsansms'
        if letra not in tipos:
            letra = pygame.font.get_default_font()
        self.tipo_letra = pygame.font.SysFont(letra, tam_letra, True)

class Marcador (Mensaje):

    def __init__(self):
        self.preparar_tipografia(TAM_LETRA_MARCADOR)
        self.reset()

    def reset(self):
        self.puntuacion = [0, 0]

    def pintame(self, pantalla: pygame.Surface):
       
        n = 1
        for punto in self.puntuacion:
            puntuacion = str(punto)            
            img_texto = self.tipo_letra.render(puntuacion, True, COLOR_OBJETOS) 
            ancho_img = img_texto.get_width() 
            x = n/4 * ANCHO - ancho_img/2 
            y = MARGEN
            pantalla.blit(img_texto,(x, y)) 
            n += 2

    def incrementar(self, jugador):
 
        if jugador in (1, 2): 
            self.puntuacion[jugador - 1] += 1 

    def quien_gana(self):

        if self.puntuacion[0] == 9:
            return 1
        if self.puntuacion[1] == 9:
            return 2
        return 0
    
class Menu_final (Mensaje):

    def __init__(self):

        self.preparar_tipografia(TAM_LETRA_MENSAJE)
    
    def pintame(self, pantalla: pygame.Surface, mensaje, separacion_centro_y, convertir_negativo):

        img_texto = self.tipo_letra.render(mensaje, True, COLOR_LETRAS)
        ancho_texto = img_texto.get_width()
        alto_texto = img_texto.get_height()
        x = (ANCHO- ancho_texto)/2
        y = ALTO/2 + (alto_texto*convertir_negativo) + separacion_centro_y
        pantalla.blit(img_texto,(x, y)) 

#       En un principio pensé en escribir los mensajes por separado y quedaba bien situado en el eje y, 
#       pero he decidido pasarlos por parámetros y queda ligeramente descolocado... Aún no sé por qué.
#       
#       El código original era este: 

#        img_texto = self.tipo_letra.render(f"El jugador {ganador} ha ganado", True, COLOR_LETRAS)
#        ancho_texto = img_texto.get_width()
#        alto_texto = img_texto.get_height()
#        x = (ANCHO- ancho_texto)/2
#        y = ALTO/2-alto_texto-15
#        pantalla.blit(img_texto,(x, y))       

#        img_texto_reinicio = self.tipo_letra.render("¿Quieres jugar otra partida? s/n", True, COLOR_LETRAS)
#        ancho_texto_reinicio = img_texto_reinicio.get_width()
#        alto_texto_reinicio = img_texto_reinicio.get_height()
#        x_reinicio = (ANCHO - ancho_texto_reinicio)/2
#        y_reinicio = ALTO/2+alto_texto_reinicio+15
#        pantalla.blit(img_texto_reinicio,(x_reinicio, y_reinicio))  

class Pong:

    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        self.pelota = Pelota()
        self.jugador1 = Jugador(MARGEN)
        self.jugador2 = Jugador(ANCHO - MARGEN - ANCHO_PALA)
        self.marcador = Marcador()
        self.menu_final = Menu_final()


    def jugar(self):
        salir = False
        
        while not salir:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE):
                    salir = True

            estado_teclas = pygame.key.get_pressed()
            if estado_teclas[pygame.K_a]:
                self.jugador1.subir()
            if estado_teclas[pygame.K_z]:
                self.jugador1.bajar()
            if estado_teclas[pygame.K_UP]:
                self.jugador2.subir()
            if estado_teclas[pygame.K_DOWN]:
                self.jugador2.bajar()

            self.pantalla.fill(COLOR_FONDO)

            self.jugador1.pintame(self.pantalla)

            self.jugador2.pintame(self.pantalla)

            self.pintar_red()


            punto_para = self.pelota.mover()
            self.pelota.pintame(self.pantalla)

            if self.pelota.colliderect(self.jugador1) or self.pelota.colliderect(self.jugador2):
                self.pelota.vel_x = -self.pelota.vel_x
                    
            if punto_para in (1,2):
                self.marcador.incrementar(punto_para)
                
            ganador = self.marcador.quien_gana()

            if ganador > 0:

                self.pelota.vel_x = self.pelota.vel_y = 0 
                
                self.menu_final.pintame(self.pantalla, f"El jugador {ganador} ha ganado la partida", -15, -1)
                self.menu_final.pintame(self.pantalla, "¿Empezar una nueva partida? (S/N)", 15, 1)                
                 
                if evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                    if ganador == 1:
                        self.marcador.reset()
                        ganador = self.marcador.quien_gana()
                        self.pelota.reiniciar(False)
                    elif ganador == 2:
                        self.marcador.reset()
                        ganador = self.marcador.quien_gana()
                        self.pelota.reiniciar(True)

                elif evento.type == pygame.KEYUP and evento.key ==pygame.K_n:
                        
                    salir = True
            
            self.marcador.pintame(self.pantalla)

            pygame.display.flip() 
            self.reloj.tick(FPS) 

        pygame.quit()

    def pintar_red(self):
        pos_x = ANCHO / 2

        tramo_pintado = 20
        tramo_vacio = 15
        ancho_red = 6

        for y in range(0, ALTO, tramo_pintado + tramo_vacio):
            pygame.draw.line(
                self.pantalla,
                COLOR_RED,
                (pos_x, y),
                (pos_x, y + tramo_pintado),
                width=ancho_red)

