from game_files.objects.creatures.creature import Creature
from game_files.astar_files.astar import a_star
from utils.frame_counter import FrameCounter
from config_files.game_settings import (
    ENEMY_START_LOCATION, RED,
    ENEMY_VELOCITY, BLOCK_SIZE,
    DEF_MAP_GRID,
    ENEMY_PATH_RESET_TIME, ENEMY_SHOOT_COOLDOWN)


class Enemy(Creature):
    def __init__(self, player, start_loc=ENEMY_START_LOCATION, shoot_cooldown=ENEMY_SHOOT_COOLDOWN, stationary=False):
        super().__init__(color=RED, start_loc=start_loc, shoot_cooldown=shoot_cooldown)
        self.player = player
        self.path_count = 0
        self.path = None
        self.path_time = 0
        self.stationary = stationary

    def attack_player(self):
        self.try_shoot(self.player.rect.center, 'e')

    def handle_movement(self):
        self.move_to_player()
        self.try_move()

    def update(self):
        if self.player.is_alive():
            self.attack_player()
        if not self.stationary:
            self.handle_movement()

    def move_to_player(self):
        if self.path is not False and (self.path is None or self.path_count == len(self.path) - 1) or FrameCounter.get_frames() - self.path_time > ENEMY_PATH_RESET_TIME:
            # print('new path')
            self.path_time = FrameCounter.get_frames()
            self.speed_x = 0
            self.speed_y = 0
            self.path_count = 0
            self.path = a_star(DEF_MAP_GRID, self.get_grid_loc(), self.player.get_grid_loc())
            if not self.path:
                return
            self.path_time = FrameCounter.get_frames()
            self.rect.x = self.path[0][0] * BLOCK_SIZE
            self.rect.y = self.path[0][1] * BLOCK_SIZE
            if len(self.path) == 1:
                self.path = False
                return

        if self.path is False:
            return

        current_step = self.path[self.path_count]
        current_loc = (current_step[0] * BLOCK_SIZE, current_step[1] * BLOCK_SIZE)

        # print(self.rect[:2], current_loc)
        if self.is_close(current_loc):
            # re-center (is fluent because the re-center distance is less than the player velocity)
            self.rect.x = current_loc[0]
            self.rect.y = current_loc[1]

            self.path_count += 1
            if self.path_count >= len(self.path):
                self.path = None
                return
            current_step = self.path[self.path_count]
            prev_place = self.path_count - 1
            dy = current_step[1] - self.path[prev_place][1]
            dx = current_step[0] - self.path[prev_place][0]

            self.speed_x = ENEMY_VELOCITY * dx
            self.speed_y = ENEMY_VELOCITY * dy

            # if self.speed_x and self.speed_y:
            #     self.speed_x *= SIN45
            #     self.speed_y *= SIN45

    def is_close(self, loc):
        dx = abs(self.rect.x - loc[0])
        dy = abs(self.rect.y - loc[1])
        d = (dx**2 + dy**2)**0.5
        return d <= round(ENEMY_VELOCITY)
