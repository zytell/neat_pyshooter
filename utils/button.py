import pygame
from config_files.neat_visual_config import (
    DEF_FONT_SIZE,
    BUTTON_TEXT_COLOR, BUTTON_COLOR1, BUTTON_COLOR2,
    FONT_TYPE
)


class Button:
    def __init__(self, text, loc, text_color=BUTTON_TEXT_COLOR, button_color1=BUTTON_COLOR1, button_color2=BUTTON_COLOR2, font_size=DEF_FONT_SIZE):
        self.text = text
        self.loc = loc
        self.text_color = text_color
        self.button_color1 = button_color1
        self.button_color2 = button_color2
        self.font_size = DEF_FONT_SIZE

        pygame.font.init()
        font = pygame.font.SysFont(FONT_TYPE, font_size)
        self.txt = font.render(text, True, text_color)
        self.size = font.size(text)  # (width, height)
        self.button_rect = pygame.Rect(self.loc[0], self.loc[1], self.size[0] + 20, self.size[1] + 5)

        # self.button_surf = pygame.Surface(self.size[0])
        self.mouse_on = False


    @staticmethod
    def point_in_rect(point, rect):
        # checks if point is in rect
        return rect.left < point[0] < rect.right and rect.top < point[1] < rect.bottom

    def blit_text(self, surf, button_rect):
        # blits text to button_surf
        draw_x = button_rect.centerx - (self.size[0] / 2.)
        draw_y = button_rect.centery - (self.size[1] / 2.)
        cords = (draw_x, draw_y)
        surf.blit(self.txt, cords)

    def draw(self, surf):

        mouse_point = pygame.mouse.get_pos()

        if not self.point_in_rect(mouse_point, self.button_rect):

            pygame.draw.rect(surf, self.button_color1, self.button_rect)
            self.blit_text(surf, self.button_rect)

        else:
            self.mouse_on = True
            pygame.draw.rect(surf, self.button_color2, self.button_rect)
            self.blit_text(surf, self.button_rect)

    def is_pressed(self, button_down):
        # only says if pressed after button is drawn.
        return self.mouse_on and button_down


