import pygame
from config_files.neat_visual_config import (
    WHITE,
    FONT_TYPE, DEF_FONT_SIZE
)


class Text:
    def __init__(self, text, pos, color=WHITE, font_size=DEF_FONT_SIZE, font_type=FONT_TYPE):
        self.x = pos[0]  # Horizontal center of box
        self.y = pos[1]  # Vertical center of box
        pygame.font.init()
        font = pygame.font.SysFont(font_type, font_size)
        self.txt = font.render(text, True, color)
        self.size = font.size(text)  # (width, height)

    # Draw Method
    def draw(self, surf):
        draw_x = self.x - (self.size[0] / 2.)
        draw_y = self.y - (self.size[1] / 2.)
        cords = (draw_x, draw_y)
        surf.blit(self.txt, cords)
