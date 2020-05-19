import pygame
import sys

from config_files.neat_config import INPUT_SIZE
from config_files.neat_visual_config import (
    WINDOW_SIZE, REFRESH_RATE,
    BACKGROUND_IMAGE, BACKGROUND_COLOR, NODE_RADIUS, LINE_WIDTH, WINDOW_WIDTH,
    WINDOW_HEIGHT, RED, NODE_COLOR, GREEN,
    BLACK, WHITE,
    SMALL_FONT_SIZE, DARK_GRAY)
from neat.genome import Genome
from neat.node_gene import NodeGene
from neat.connection_gene import ConnectionGene
from neat.neat_visual.centered_text import Text
from utils.button import Button


class Visual:

    def __init__(self, genome: Genome):
        pygame.init()
        self.main_surf = pygame.Surface(WINDOW_SIZE)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.genome = genome
        self.main_loop()

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    @staticmethod
    def get_node_pos(node):
        return int(node.x * WINDOW_WIDTH), int(node.y * WINDOW_HEIGHT)

    def draw_genome(self):
        # draw connections:
        con: ConnectionGene
        for con in self.genome.connections.data:
            start_pos = self.get_node_pos(con.prev)
            end_pos = self.get_node_pos(con.next)
            con_weight = con.weight
            if con.enabled:
                if con_weight > 0:
                    line_color = GREEN
                else:
                    line_color = RED
            else:
                line_color = DARK_GRAY

            pygame.draw.line(self.main_surf, line_color, start_pos, end_pos, LINE_WIDTH)

            con_centerx = (start_pos[0] + end_pos[0]) / 2
            con_centery = (start_pos[1] + end_pos[1]) / 2

            rounded_weight = round(con.weight, 4)

            innov_text = Text(str(con.innovation_num), (con_centerx, con_centery - NODE_RADIUS), color=WHITE, font_size=SMALL_FONT_SIZE)
            weight_text = Text(str(rounded_weight), (con_centerx, con_centery + NODE_RADIUS), color=line_color, font_size=SMALL_FONT_SIZE)

            innov_text.draw(self.main_surf)
            weight_text.draw(self.main_surf)

        # draw nodes:
        node: NodeGene
        for node in self.genome.nodes.data:
            pos = self.get_node_pos(node)
            pygame.draw.circle(self.main_surf, NODE_COLOR, pos, NODE_RADIUS, 0)
            node_num_text = Text(str(node.innovation_num), pos, color=BLACK)
            node_num_text.draw(self.main_surf)

    def main_loop(self):

        while True:
            button_down = False

            # keep loop running at the right speed
            self.clock.tick(REFRESH_RATE)
            # process input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:  # some key actions
                    if pygame.key.get_pressed()[pygame.K_e]:
                        print('pressed "e"')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        button_down = True

            # --- graphics update --- #

            if BACKGROUND_IMAGE:  # delete last frame by blitting background:
                self.main_surf.blit(BACKGROUND_IMAGE, (0, 0))
            else:  # if there's no background, blit def bg color.
                self.main_surf.fill(BACKGROUND_COLOR)

            # --- drawing stuff --- #
            self.draw_genome()
            commands = {
                'random weight': self.genome.mutate_weight_random,
                'weight shift': self.genome.mutate_weight_shift,
                'link mutate': self.genome.mutate_link,
                'node mutate': self.genome.mutate_node,
                'on / off': self.genome.mutate_link_toggle,
                'mutate random': self.genome.mutate_random,
                'calculate': self.genome.calculate
            }
            x = 20
            y = 20

            for text, command in commands.items():
                b = Button(text, (x, y), font_size=18)
                b.draw(self.main_surf)
                if b.is_pressed(button_down):
                    if text == 'calculate':
                        self.genome.generate_calculator()
                        print(self.genome.calculate(lst=([1] * INPUT_SIZE)))
                    else:
                        command()
                x += b.button_rect.size[0] + 20

            # after drawing, flip the display
            self.screen.blit(self.main_surf, (0, 0))
            pygame.display.flip()
