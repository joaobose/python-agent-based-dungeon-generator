from os import path

WIDTH, HEIGHT = 1600, 1400

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

# ROOM COLORS

R_START = WHITE
R_BOSS = RED

R_KEY = ROSADO_GAY

R_WEAPON = (144, 238, 144)
R_WEAPON_UPGRADE = (76, 187, 23)
R_PASSIVE = (138, 154, 91)
R_PLAYER_BUFF = (53, 94, 59)

R_STORE = BLUE

# GENERATION QUEUE

# (ROOM_TYPE, POSSIBLE_SIZES, ALLOW_EXPANSION)
GENERATION_QUEUE = [
    (R_BOSS, [32], False),
    (R_KEY, [24, 28], True),
    (R_WEAPON, [16, 24], True),
    (R_KEY, [24, 28], True),
    (R_WEAPON_UPGRADE, [16, 24], True),
    (R_KEY, [24, 28], True),
    (R_PASSIVE, [16, 24], True),
    (R_PLAYER_BUFF, [16, 24], True),
    (R_STORE, [10], True)
]

assert len(GENERATION_QUEUE) == N_ROOMS - 1
