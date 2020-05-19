from game_files.objects.wall import Wall
from config_files.game_settings import (
    BLOCK_SIZE, DEF_MAP_GRID
)


class Map:
    def __init__(self, grid=None):
        self.walls = list()
        if not grid:
            self.grid = DEF_MAP_GRID
        else:
            self.grid = grid

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[j][i]:  # isn't empty
                    self.walls.append(Wall(start_loc=(i * BLOCK_SIZE, j * BLOCK_SIZE), topleft=True))


