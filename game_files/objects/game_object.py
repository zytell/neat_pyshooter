import pygame
from config_files.game_settings import (
    PLAYER_START_LOCATION, DEF_COLOR, DEF_OBJ_SIZE,
    BLOCK_SIZE
)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, start_loc=None, color=None, size=None, bottomright=False, topleft=False, **kwargs):
        super().__init__()
        if not start_loc:
            start_loc = PLAYER_START_LOCATION
        if not color:
            color = DEF_COLOR
        if not size:
            size = DEF_OBJ_SIZE
        self.image = pygame.Surface(size)
        self.image.fill(color)
        if bottomright:
            self.rect = self.image.get_rect(bottomright=start_loc)
        elif topleft:
            self.rect = self.image.get_rect(topleft=start_loc)
        else:
            self.rect = self.image.get_rect(center=start_loc)
        self.speed_x = 0
        self.speed_y = 0

    def get_grid_loc(self):
        return self.rect.centerx // BLOCK_SIZE, self.rect.centery // BLOCK_SIZE

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
