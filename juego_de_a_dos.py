import pygame
import sys
from module_juegoSnake import Display, Mapa, Comida, Snake

class Jugador():
    def __init__(self, color):
        self.color = color

class DisplayDeADos():
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
        self.yellow = pygame.Color(255, 255, 0)

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
            self.dibujar(snake.color, segmento[0]*self.block_width, segmento[1]*self.block_height, self.block_width, self.block_height)

    def dibujar_comida(self, comida):
        self.dibujar(self.green, comida.pos[0]*self.block_width, comida.pos[1]*self.block_height, self.block_width, self.block_height)

    def resetear_ventana(self):
        self.game_window.fill(self.black)

    def escribir_jugador(self, fuente, jugador):
        fuente_jugador = pygame.font.SysFont(fuente, 90)
        imagen_jugador = fuente_jugador.render(f"VICTORIA DEL {jugador.nombre.upper()}", True, jugador.color)

        rect_jugador = imagen_jugador.get_rect()
        rect_jugador.midtop = (self.width/2, self.height/4)

        self.game_window.blit(imagen_jugador, rect_jugador)

    def escribir_empate(self, fuente):
        fuente_empate = pygame.font.SysFont(fuente, 90)
        imagen_empate = fuente_empate.render(f"EMPATE", True, self.blue)

        rect_empate = imagen_empate.get_rect()
        rect_empate.midtop = (self.width/2, self.height/4)

        self.game_window.blit(imagen_empate, rect_empate)

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

    def mostrar_jugador(self, ganador, puntaje1, puntaje2):
        self.game_window.fill(self.black)

        fuente = "times new roman"
        self.escribir_jugador(fuente, ganador)
        self.escribir_reiniciar_salir(fuente, ganador.color)
        self.escribir_puntajes_finales(fuente, puntaje1, puntaje2)

        pygame.display.update()

    def mostrar_empate(self, puntaje1, puntaje2):
        self.game_window.fill(self.black)

        fuente = "times new roman"
        self.escribir_empate(fuente)
        self.escribir_reiniciar_salir(fuente, self.blue)
        self.escribir_puntajes_finales(fuente, puntaje1, puntaje2)

        pygame.display.update()

    def escribir_puntaje_juego(self, fuente, x, y, puntaje, color):
        fuente_puntaje = pygame.font.SysFont(fuente, 30)
        imagen_puntaje = fuente_puntaje.render(f"Puntaje = {puntaje}", True, color)

        rect_puntaje = imagen_puntaje.get_rect()
        rect_puntaje.topleft = (x, y)

        self.game_window.blit(imagen_puntaje, rect_puntaje)

    def escribir_puntajes_finales(self, fuente, puntaje1, puntaje2):
        fuente_puntaje1 = pygame.font.SysFont(fuente, 45)
        imagen_puntaje1 = fuente_puntaje1.render(f"Puntaje = {puntaje1}", True, self.white)

        rect_puntaje1 = imagen_puntaje1.get_rect()
        rect_puntaje1.midtop = (self.width/2 - 200, 1.5*self.height/4 + 50)

        self.game_window.blit(imagen_puntaje1, rect_puntaje1)

        fuente_puntaje2 = pygame.font.SysFont(fuente, 45)
        imagen_puntaje2 = fuente_puntaje2.render(f"Puntaje = {puntaje2}", True, self.yellow)

        rect_puntaje2 = imagen_puntaje2.get_rect()
        rect_puntaje2.midtop = (self.width/2 + 200, 1.5*self.height/4 + 50)

        self.game_window.blit(imagen_puntaje2, rect_puntaje2)

class JuegoDeADos():
    def __init__(self, display: DisplayDeADos, fps, game_width, game_height):
        self.display = display
        self.fps = fps
        self.game_width = game_width
        self.game_height = game_height

    def choco_con_borde(self, snake):
        return self.mapa.detectar_borde(snake.cabeza)
    
    def choco_con_otro_snake(self, snake, otro_snake):
        return snake.cabeza in otro_snake.obtener_posiciones()

    def snake_muere(self, snake1, snake2):
        return self.choco_con_borde(snake1) or snake1.choco_con_segmento() or self.choco_con_otro_snake(snake1, snake2)

    def perdio_juego(self):
        return (self.mapa.detectar_borde(self.jugador_1.cabeza)) or (self.jugador_1.choco_con_segmento())

    def gano_juego(self):
        return self.jugador_1.longitud() >= self.mapa.casillas

    def quien_gano(self, snake1, snake2):
        if self.snake_muere(snake1, snake2) and not self.snake_muere(snake2, snake1):
            return snake2
        elif self.snake_muere(snake2, snake1) and not self.snake_muere(snake1, snake2):
            return snake1
    
    def hay_empate(self, snake1, snake2):
        return self.snake_muere(snake1, snake2) and self.snake_muere(snake2, snake1)

    def termino_juego(self):
        return self.snake_muere(self.jugador_1, self.jugador_2) or self.snake_muere(self.jugador_2, self.jugador_1)
    
    def comida_en_snake(self, snake):
        return self.comida.obtener_posicion() in snake.obtener_posiciones()
    
    def cambiar_direccion_1(self, keys):
        for event in keys:
            if event.key == pygame.K_UP:
                self.jugador_1.cambiar_direccion("ARRIBA")
            if event.key == pygame.K_DOWN:
                self.jugador_1.cambiar_direccion("ABAJO")
            if event.key == pygame.K_LEFT:
                self.jugador_1.cambiar_direccion("IZQUIERDA")
            if event.key == pygame.K_RIGHT:
                self.jugador_1.cambiar_direccion("DERECHA")
            break

    def cambiar_direccion_2(self, keys):
        for event in keys:
            if event.key == ord('w'):
                self.jugador_2.cambiar_direccion("ARRIBA")
            if event.key == ord('s'):
                self.jugador_2.cambiar_direccion("ABAJO")
            if event.key == ord('a'):
                self.jugador_2.cambiar_direccion("IZQUIERDA")
            if event.key == ord('d'):
                self.jugador_2.cambiar_direccion("DERECHA")
            break

    def obtener_teclas_1(self, keys, event):
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            keys.append(event)
        return keys

    def obtener_teclas_2(self, keys, event):
        if event.key == ord('w') or event.key == ord('s') or event.key == ord('a') or event.key == ord('d'):
            keys.append(event)
        return keys
        
    def cambiar_direcciones(self):
        keys_snake_1 = []
        keys_snake_2 = []

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                keys_snake_1 = self.obtener_teclas_1(keys_snake_1, event)
                keys_snake_2 = self.obtener_teclas_2(keys_snake_2, event)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.cambiar_direccion_1(keys_snake_1)
        self.cambiar_direccion_2(keys_snake_2)

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
        self.cambiar_direcciones()
        self.jugador_1.mover()
        self.jugador_2.mover()
        if self.comida_en_snake(self.jugador_1):
            self.jugador_1.crecer()
            self.comida.aparecer_comida()
            while self.comida_en_snake(self.jugador_1):
                self.comida.aparecer_comida()
        if self.comida_en_snake(self.jugador_2):
            self.jugador_2.crecer()
            self.comida.aparecer_comida()
            while self.comida_en_snake(self.jugador_2):
                self.comida.aparecer_comida()
    
        self.display.resetear_ventana()
        self.display.dibujar_snake(self.jugador_1)
        self.display.dibujar_snake(self.jugador_2)
        self.display.dibujar_comida(self.comida)
        self.display.escribir_puntaje_juego("times new roman", 10, 5, self.obtener_puntaje(self.jugador_1), self.jugador_1.color)
        self.display.escribir_puntaje_juego("times new roman", 200, 5, self.obtener_puntaje(self.jugador_2), self.jugador_2.color)
        pygame.display.update()
        self.fps_controller.tick(self.difficulty)

    def obtener_puntaje(self, snake):
        return len(snake.obtener_posiciones()) - 2

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
            self.jugador_1 = Snake(self.game_width//6, self.game_height//4, self.display.white, "Jugador 1")
            self.jugador_2 = Snake(self.game_width//6, self.game_height//4 - 2, self.display.yellow, "Jugador 2")
            

            while not self.termino_juego():
                self.jugar_hasta_que_termine()

            if self.hay_empate(self.jugador_1, self.jugador_2):
                self.display.mostrar_empate(self.obtener_puntaje(self.jugador_1), self.obtener_puntaje(self.jugador_2))
                pass
            else:
                self.display.mostrar_jugador(self.quien_gano(self.jugador_1, self.jugador_2), self.obtener_puntaje(self.jugador_1), self.obtener_puntaje(self.jugador_2))

            self.reiniciar()

game_width = 32
game_height = 18

block_width = 40
block_height = 40

display = DisplayDeADos(game_width, game_height, block_width, block_height)
juego = JuegoDeADos(display, 10, game_width, game_height)

juego.jugar()