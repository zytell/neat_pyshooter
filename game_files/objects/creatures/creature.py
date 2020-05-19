import pygame
from game_files.objects.game_object import GameObject
from game_files.objects.bullet import Bullet
from config_files.game_settings import (
    all_sprites, enemy_bullets, walls, BULLET_VELOCITY,
    DEF_SHOOT_COOLDOWN, DEF_HP, player_bullets, DEF_MAP_GRID
    )
from config_files.smart_bot_config import (
    VISION_RADIUS,
    SEE_LEN)

from utils.frame_counter import FrameCounter


# need to implement face direction
class Creature(GameObject):
    def __init__(self, shoot_cooldown=DEF_SHOOT_COOLDOWN, hp=DEF_HP, **kwargs):
        super().__init__(**kwargs)
        self.last_shoot = 0
        self.shoot_cooldown = shoot_cooldown
        self.hp = hp

    def get_surrounding(self, radius=VISION_RADIUS):
        map_grid = DEF_MAP_GRID
        grid_x, grid_y = self.get_grid_loc()
        x_border = len(map_grid[0])
        y_border = len(map_grid)

        surrounding = list()

        for y in range(grid_y - radius, grid_y + radius + 1):
            for x in range(grid_x - radius, grid_x + radius + 1):
                if not (0 <= x < x_border and 0 <= y < y_border):
                    surrounding.append(0.5)
                else:
                    surrounding.append(map_grid[y][x])
        surrounding[VISION_RADIUS + SEE_LEN * VISION_RADIUS] = 0.5
        return surrounding

    def print_surrounding(self, radius=VISION_RADIUS):

        surrounding = self.get_surrounding(radius)

        length = radius * 2 + 1
        print('# ------------------------- #')
        for i in range(0, length**2, length):
            print(surrounding[i: i + length])

    @staticmethod
    def get_grid_distance(loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    def surrounding_with_bullets(self, radius=VISION_RADIUS):
        map_grid = [x[:] for x in DEF_MAP_GRID]

        bullet: Bullet
        bot_loc = self.get_grid_loc()
        for bullet in self.bullet_sprites:
            # TODO: implement bullet direction in range -0.5 < dir < 0
            # bullet_dir = bullet.speed_y + bullet.speed_x

            bullet_loc = bullet.get_grid_loc()
            if self.get_grid_distance(bullet_loc, bot_loc) <= VISION_RADIUS:
                if not map_grid[bullet_loc[1]][bullet_loc[0]]:  # bullet may collide with wall, if so it disappears.
                    map_grid[bullet_loc[1]][bullet_loc[0]] = -1

        grid_x, grid_y = self.get_grid_loc()
        x_border = len(map_grid[0])
        y_border = len(map_grid)

        surrounding = list()

        for y in range(grid_y - radius, grid_y + radius + 1):
            for x in range(grid_x - radius, grid_x + radius + 1):
                if not (0 <= x < x_border and 0 <= y < y_border):  # if the point is out of map bounds
                    surrounding.append(1)
                else:
                    point = map_grid[y][x]
                    if point:
                        surrounding.append(point)
                    else:
                        surrounding.append(0)

        surrounding[VISION_RADIUS + SEE_LEN * VISION_RADIUS] = 1

        return surrounding

    def get_closest_enemy_dist(self):
        if len(self.enemies) == 0:
            return 0, 0
        max_dist = 'large'
        closest_enemy_dist = None
        for enemy in self.enemies:
            enemy_loc = enemy.get_grid_loc()
            self_loc = self.get_grid_loc()
            dx = self_loc[0] - enemy_loc[0]
            dy = self_loc[1] - enemy_loc[1]
            dist = abs(dx) + abs(dy)  # for grid... thats why theres no square
            if max_dist == 'large' or dist > max_dist:
                max_dist = dist
                closest_enemy_dist = [dx, dy]  # TODO: same as bullet, give direction.

        return closest_enemy_dist

    def print_surrounding_with_bullets(self, radius=VISION_RADIUS):
        surrounding = self.surrounding_with_bullets(radius)

        length = radius * 2 + 1
        print('# ------------------------- #')
        for i in range(0, length ** 2, length):
            print(surrounding[i: i + length])

    def hurt(self):
        # hurts, and kills creature if necessary
        self.hp -= 1
        if self.hp == 0:
            self.kill()

    def try_shoot(self, target, origin='p'):
        # tries shooting - may not shoot because of cooldown

        # "frames" is frames elapsed from game start
        now = FrameCounter.get_frames()

        dt = now - self.last_shoot

        if 0 <= dt < self.shoot_cooldown:
            # if cooldown has not passed yet, don't shoot
            return
        # update last shot to now
        self.last_shoot = now

        # calculate vector for bullet
        dist_vector = (target[0] - self.rect.centerx, target[1] - self.rect.centery)
        norm = (dist_vector[0]**2 + dist_vector[1]**2) ** 0.5
        if norm != 0:
            direction = (dist_vector[0] * BULLET_VELOCITY / norm, dist_vector[1] * BULLET_VELOCITY / norm)
            rounded_direction = (round(direction[0]), direction[1])

        else:
            rounded_direction = (0, 0)

        # create bullet object and add to sprites
        bullet = Bullet(self.rect.center, rounded_direction)
        if origin == 'p':
            player_bullets.add(bullet)
        elif origin == 'e':
            enemy_bullets.add(bullet)
        all_sprites.add(bullet)

    def wall_collide_x(self):
        # checks for x-axis wall collision, moves object backwards if there is one
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for col in collisions:
            if self.speed_x > 0:
                self.rect.right = col.rect.left
            elif self.speed_x < 0:
                self.rect.left = col.rect.right

    def wall_collide_y(self):
        # checks for x-axis wall collision, moves object backwards if there is one
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for col in collisions:
            if self.speed_y < 0:
                self.rect.top = col.rect.bottom
            elif self.speed_y > 0:
                self.rect.bottom = col.rect.top

    def try_move(self):
        # tries moving creature according to speed and wall collisions
        self.rect.y += self.speed_y
        self.wall_collide_y()
        self.rect.x += self.speed_x
        self.wall_collide_x()

    def is_alive(self):
        return self.hp > 0

    def update(self):
        self.try_move()
