import pygame
from config_files.game_settings import (
    PLAYER_RIGHT, PLAYER_VELOCITY, PLAYER_DOWN,
    PLAYER_LEFT, PLAYER_UP, SIN45, LEFT_BUTTON
)
from game_files.objects.creatures.creature import Creature


class Player(Creature):
    # sprite for the player

    def __init__(self, bullet_sprites, enemy_sprites):
        super().__init__()
        # self.bullet_sprites = bullet_sprites
        # self.enemies = enemy_sprites

    def update(self):
        # self.print_surrounding_with_bullets()
        # print(self.get_closest_enemy_dist())
        self.handle_movement()
        self.handle_shooting()

    def handle_movement(self):
        self.speed_x = 0
        self.speed_y = 0
        # can_move_dirs = self.can_move()
        keystate = pygame.key.get_pressed()
        if keystate[PLAYER_UP]:
            self.speed_y -= PLAYER_VELOCITY
        if keystate[PLAYER_DOWN]:
            self.speed_y += PLAYER_VELOCITY
        if keystate[PLAYER_LEFT]:
            self.speed_x -= PLAYER_VELOCITY
        if keystate[PLAYER_RIGHT]:
            self.speed_x += PLAYER_VELOCITY

        if self.speed_x and self.speed_y:
            self.speed_x *= SIN45
            self.speed_y *= SIN45

        self.try_move()

    def handle_shooting(self):
        if pygame.mouse.get_pressed()[LEFT_BUTTON]:
            mouse_pos = pygame.mouse.get_pos()
            self.try_shoot(mouse_pos, 'p')








