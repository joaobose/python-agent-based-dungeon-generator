from os import path

WIDTH, HEIGHT = 1400, 1000

FPS = 60
NAME = "test"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (155, 155, 155)
ROSADO_GAY = (255, 100, 255)

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "pngs")
snd_folder = path.join(game_folder, "snds")

N_ROOMS = 10
