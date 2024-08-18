from module_juegoSnake import Display, Juego

game_width = 32
game_height = 18

block_width = 40
block_height = 40

display = Display(game_width, game_height, block_width, block_height)
juego = Juego(display, 10, game_width, game_height)

juego.jugar()