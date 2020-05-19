from game_files.objects.game_object import GameObject
from config_files.game_settings import (
    ORANGE, DEF_BULLET_SIZE
)


class Bullet(GameObject):
    def __init__(self, start_loc, direction=(0, 0), size=DEF_BULLET_SIZE, origin=None):
        super().__init__(start_loc=start_loc, color=ORANGE, size=size)
        self.speed_x, self.speed_y = direction
