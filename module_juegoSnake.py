import pygame
import sys
import random

class Comida():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.aparecer_comida()

    def aparecer_comida(self):
        self.pos = [random.randint(1, self.width-1), random.randint(1, self.height-1)]

    def obtener_posicion(self):
        return self.pos
    
class Mapa():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.casillas = (self.width)*(self.height)
    
    def detectar_borde(self, pos):
        return (pos[0] == -1 or pos[0] == self.width + 1) or (pos[1] == -1 or pos[1] == self.height + 1)

class Snake():
    def __init__(self, x, y):
        self.cabeza = [x+1, y]
        self.direccion = "DERECHA"
        self.cuerpo = [[x, y]]

    def mover(self):
        for pos in range(len(self.cuerpo)-1, 0, -1):
            self.cuerpo[pos] = self.cuerpo[pos - 1].copy()
        self.cuerpo[0] = self.cabeza.copy()
        if self.direccion == "DERECHA":
            self.cabeza[0] += 1
        elif self.direccion == "IZQUIERDA":
            self.cabeza[0] -= 1
        elif self.direccion == "ABAJO":
            self.cabeza[1] += 1
        elif self.direccion == "ARRIBA":
            self.cabeza[1] -= 1
        else:
            pass
        
    def cambiar_direccion(self, direccion):
        if self.direccion == "DERECHA" and direccion != "IZQUIERDA":
            self.direccion = direccion
        elif self.direccion == "IZQUIERDA" and direccion != "DERECHA":
            self.direccion = direccion
        elif self.direccion == "ARRIBA" and direccion != "ABAJO":
            self.direccion = direccion
        elif self.direccion == "ABAJO" and direccion != "ARRIBA":
            self.direccion = direccion
        else:
            pass

    def crecer(self):
        self.cuerpo.append(self.cuerpo[-1].copy())

    def obtener_posiciones(self):
        posiciones = [self.cabeza]
        for pos in self.cuerpo:
            posiciones.append(pos)
        return posiciones
        
    def choco_con_segmento(self):
        return self.cabeza in self.cuerpo
    
    def longitud(self):
        return len(self.cuerpo) + 1

class Display():
    def __init__(self, game_width, game_height, block_width, block_height):

        self.game_width = game_width
        self.game_height = game_height

        self.block_width = block_width
        self.block_height = block_height

        self.width = self.game_width * self.block_width
        self.height = self.game_height * self.block_height

        # colores
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

    def iniciar_ventana(self):
        # chequear errores
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Se encontraron {check_errors[1]} errores iniciando el juego, saliendo...')
            sys.exit(-1)
        else:
            print('[+] Juego iniciado con 0 errores')

        # inicializar la ventana
        pygame.display.set_caption('Snake')
        self.icon = pygame.image.load('snake.png')
        pygame.display.set_icon(self.icon)
        self.game_window = pygame.display.set_mode((self.width, self.height))

    def dibujar(self, color, x, y, width, height):
        pygame.draw.rect(self.game_window, color, pygame.Rect(x, y, width, height))

    def dibujar_snake(self, snake):
        for segmento in snake.obtener_posiciones():
            self.dibujar(self.white, segmento[0]*self.block_width, segmento[1]*self.block_height, self.block_width, self.block_height)

    def dibujar_comida(self, comida):
        self.dibujar(self.green, comida.pos[0]*self.block_width, comida.pos[1]*self.block_height, self.block_width, self.block_height)

    def resetear_ventana(self):
        self.game_window.fill(self.black)

    def escribir_game_over(self, fuente):
        fuente_game_over = pygame.font.SysFont(fuente, 90)
        imagen_game_over = fuente_game_over.render("GAME OVER", True, self.red)

        rect_game_over = imagen_game_over.get_rect()
        rect_game_over.midtop = (self.width/2, self.height/4)

        self.game_window.blit(imagen_game_over, rect_game_over)

    def escribir_victoria(self, fuente):
        fuente_victoria = pygame.font.SysFont(fuente, 90)
        imagen_victoria = fuente_victoria.render("VICTORIA", True, self.green)

        rect_victoria = imagen_victoria.get_rect()
        rect_victoria.midtop = (self.width/2, self.height/4)

        self.game_window.blit(imagen_victoria, rect_victoria)

    def escribir_reiniciar_salir(self, fuente, color):

        fuente_reintentar_salir = pygame.font.SysFont(fuente, 60)
        imagen_reiniciar = fuente_reintentar_salir.render("Presione R para jugar de nuevo", True, color)
        imagen_salir = fuente_reintentar_salir.render("Presione ESC para salir", True, color)

        rect_reiniciar = imagen_reiniciar.get_rect()
        rect_reiniciar.midtop = (self.width/2, 2.5*self.height/4)
        rect_salir = imagen_salir.get_rect()
        rect_salir.midtop = (self.width/2, rect_reiniciar.bottom+10)

        self.game_window.blit(imagen_reiniciar, rect_reiniciar)
        self.game_window.blit(imagen_salir, rect_salir)

    def mostrar_game_over(self, puntaje):
        self.game_window.fill(self.black)

        fuente = "times new roman"
        self.escribir_game_over(fuente)
        self.escribir_reiniciar_salir(fuente, self.red)
        self.escribir_puntaje_final(fuente, self.red, puntaje)

        pygame.display.update()

    def mostrar_victoria(self, puntaje):
        self.game_window.fill(self.black)

        fuente = "times new roman"
        self.escribir_victoria(fuente)
        self.escribir_reiniciar_salir(fuente, self.green)
        self.escribir_puntaje_final(fuente, self.green, puntaje)

        pygame.display.update()

    def escribir_puntaje_juego(self, fuente, x, y, puntaje):
        fuente_puntaje = pygame.font.SysFont(fuente, 30)
        imagen_puntaje = fuente_puntaje.render(f"Puntaje = {puntaje}", True, self.blue)

        rect_puntaje = imagen_puntaje.get_rect()
        rect_puntaje.topleft = (x, y)

        self.game_window.blit(imagen_puntaje, rect_puntaje)

    def escribir_puntaje_final(self, fuente, color, puntaje):
        fuente_puntaje = pygame.font.SysFont(fuente, 45)
        imagen_puntaje = fuente_puntaje.render(f"Puntaje = {puntaje}", True, color)

        rect_puntaje = imagen_puntaje.get_rect()
        rect_puntaje.midtop = (self.width/2, 1.5*self.height/4)

        self.game_window.blit(imagen_puntaje, rect_puntaje)

class Juego():
    def __init__(self, display: Display, fps, game_width, game_height):
        self.display = display
        self.fps = fps
        self.game_width = game_width
        self.game_height = game_height

    def perdio_juego(self):
        return (self.mapa.detectar_borde(self.snake.cabeza)) or (self.snake.choco_con_segmento())

    def gano_juego(self):
        return self.snake.longitud() >= self.mapa.casillas
    
    def termino_juego(self):
        return self.perdio_juego() or self.gano_juego()
    
    def comida_en_snake(self):
        return self.comida.obtener_posicion() in self.snake.obtener_posiciones()
    
    def cambiar_direccion(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.snake.cambiar_direccion("ARRIBA")
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.snake.cambiar_direccion("ABAJO")
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.snake.cambiar_direccion("IZQUIERDA")
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.snake.cambiar_direccion("DERECHA")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # elif event.key == ord('g'):
                #     while not self.gano_juego():
                #         self.snake.crecer()
                break

    def reiniciar(self):
        reiniciar = False
        while not reiniciar:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == ord('r'):
                    reiniciar = True
                    break
    
    def jugar_hasta_que_termine(self):
        self.cambiar_direccion()
        self.snake.mover()
        if self.comida_en_snake():
            self.snake.crecer()
            self.comida.aparecer_comida()
            while self.comida_en_snake():
                self.comida.aparecer_comida()
    
        self.display.resetear_ventana()
        self.display.dibujar_snake(self.snake)
        self.display.dibujar_comida(self.comida)
        self.display.escribir_puntaje_juego("times new roman", 10, 5, self.obtener_puntaje())
        pygame.display.update()
        self.fps_controller.tick(self.difficulty)

    def obtener_puntaje(self):
        return len(self.snake.obtener_posiciones()) - 2

    def jugar(self):
        # dificultad
        # easy -> 10
        # medium -> 25
        # hard -> 40
        # harder -> 60
        # impossible -> 120
        self.difficulty = self.fps

        self.display.iniciar_ventana()

        # control de FPS
        self.fps_controller = pygame.time.Clock()
        while True:
            self.comida = Comida(self.game_width, self.game_height)
            self.mapa = Mapa(self.game_width-1, self.game_height-1)
            self.snake = Snake(self.game_width//6, self.game_height//4)
            
            while not self.termino_juego():
                self.jugar_hasta_que_termine()

            if self.perdio_juego():
                self.display.mostrar_game_over(self.obtener_puntaje())
        
            elif self.gano_juego():
                self.display.mostrar_victoria(self.obtener_puntaje())

            self.reiniciar()