import sys
import pygame
import pickle
from utils.frame_counter import FrameCounter
from neat.neat_visual.visual import Visual
from game_files.objects.creatures.player import Player
from game_files.objects.creatures.enemy import Enemy
from game_files.map import Map
from config_files.game_settings import (
    window_size, CAPTION,
    REFRESH_RATE, all_sprites, enemies, enemy_bullets,
    player_bullets, walls, BACKGROUND_IMAGE
)

from game_files.objects.creatures.smart_bot import SmartBot

high_refresh = False  # makes game run faster ONLY when display is active
learning_mode = True  # quits game when player dies.
client_mode = True  # decides whether the client (computer) will play, or the player.
display_active = True  # can disable graphics, makes game run MUCH faster - for learning.
load_client_mode = True  # choose whether to load a client or start new learning
load_client_visual = False  # show client genome visual representation

# client path is a variable for the path of the client to load.
client_path = 'saved/20200519-201434/82/client.pkl'

if not display_active and not client_mode:
    raise Exception('Error, player cannot play without display (no input)')

# initialization of pygame and variables
pygame.init()
# display initialized later to enable disabling graphics.
main_surf = pygame.Surface(window_size)
clock = pygame.time.Clock()


# window title caption
pygame.display.set_caption(CAPTION)

# sprites management
if client_mode:
    player_sprite = SmartBot(enemy_bullets, enemies, None)
else:
    player_sprite = Player(enemy_bullets, enemies)

if high_refresh:
    REFRESH_RATE = 4000
e = Enemy(player_sprite)
all_sprites.add(e)
enemies.add(e)

all_sprites.add(player_sprite)


# default map
def_map = Map()
walls.add(def_map.walls)
all_sprites.add(walls)


def handle_collisions():
    # if bullet collides with enemy, kill bullet and hurt enemy
    enemy_hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
    if player_sprite.hp > 0:
        player_hits = pygame.sprite.spritecollide(player_sprite, enemy_bullets, True)
    else:
        player_hits = None
    for enemy in enemy_hits:
        enemy.hurt()
    if player_hits:
        player_sprite.hurt()

    # if player/enemy bullet collides with wall, kill bullet
    pygame.sprite.groupcollide(enemy_bullets, walls, True, False)
    pygame.sprite.groupcollide(player_bullets, walls, True, False)


def terminate():
    pygame.quit()
    sys.exit()


def load_client(path, show_genome=False):
    # load a saved client:
    with open(path, 'rb') as inp:
        client = pickle.load(inp)
    if show_genome:
        Visual(client.genome)
    return client


def main(client=None):

    # load a saved client:
    if load_client_mode is True:
        client = load_client(client_path, load_client_visual)
        # print('species score:', client.species.score)
        # print('expected client score: %s' % client.score)

    # to prevent collection of too many frames:
    FrameCounter.reset_frames()
    if not client or display_active:
        screen = pygame.display.set_mode(window_size)

    if learning_mode and False:
        for enemy in enemies:
            enemy.stationary = True

    if client_mode and client:
        player_sprite.client = client

    while True:
        # keep loop running at the right speed
        if display_active:
            clock.tick(REFRESH_RATE)
        FrameCounter.add_frame()
        # process input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:  # some key actions
                if pygame.key.get_pressed()[pygame.K_e]:
                    print('enemy created')
                    e = Enemy(player_sprite)
                    enemies.add(e)
                    all_sprites.add(e)
                elif pygame.key.get_pressed()[pygame.K_r]:
                    print('player hp: %s' % player_sprite.hp)
                    if not player_sprite.alive():
                        print('player dead, reviving')
                        player_sprite.__init__(enemy_bullets, enemies)
                        all_sprites.add(player_sprite)

        # update
        all_sprites.update()
        handle_collisions()

        if learning_mode and not player_sprite.is_alive():
            score = FrameCounter.get_frames()
            [s.kill() for s in all_sprites.sprites()]
            if load_client_mode:
                print('calculated score: %s\n' % score)
            return score
        if client and client_mode:
            frames = FrameCounter.get_frames() % 10
            if frames == 0 or frames == 5:
                # AI makes decision only once every 5 frames - more efficient.
                inputs = list()
                inputs += player_sprite.surrounding_with_bullets()
                enemy_dist = player_sprite.get_closest_enemy_dist()
                inputs += enemy_dist
                player_sprite.act(node_input=inputs)

        if not display_active:
            continue

        # draw / render
        main_surf.blit(BACKGROUND_IMAGE, (0, 0))
        all_sprites.draw(main_surf)
        screen.blit(main_surf, (0, 0))

        # after drawing, flip the display
        pygame.display.flip()


if __name__ == '__main__':
    raise Exception('Please run program from game_learning.py')
