import pygame

CAPTION = "SPACE ZOMBIE SHOOTER 3"
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
REFRESH_RATE = 60

# ----object stuff:
DEF_OBJ_SIZE = (50, 50)
DEF_BULLET_SIZE = (20, 20)
BULLET_VELOCITY = 4
DEF_SHOOT_COOLDOWN = 20  # in frames
ENEMY_SHOOT_COOLDOWN = 45
DEF_HP = 5
BLOCK_SIZE = 50
DEF_MAP_SIZE = 13

# --sprites management:
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

# --player variables-- :
# player start location
PLAYER_START_LOCATION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
# player velocity (px/sec)
PLAYER_VELOCITY = 5
ENEMY_VELOCITY = 3
SIN45 = 0.85090352453
ENEMY_PATH_RESET_TIME = 200

# --enemy variables:
ENEMY_START_LOCATION = (WINDOW_WIDTH / 2, WINDOW_WIDTH / 4)

# KEYS:
PLAYER_UP = pygame.K_w
PLAYER_DOWN = pygame.K_s
PLAYER_LEFT = pygame.K_a
PLAYER_RIGHT = pygame.K_d

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
NICE_GREEN = (20, 100, 20)
BLUE = (0, 0, 255)
ORANGE = (255, 125, 0)

DEF_COLOR = BLUE

# game font
pygame.font.init()
FONT = pygame.font.SysFont('comicsansms', 34)

# BUTTONS:
LEFT_BUTTON = 0
SCROLL = 1
RIGHT_BUTTON = 0

# image loading
BACKGROUND_IMAGE = pygame.Surface(window_size)
BACKGROUND_IMAGE.fill(NICE_GREEN)

DEF_MAP_GRID = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]


