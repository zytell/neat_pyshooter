from game_files.objects.creatures.creature import Creature
from config_files.game_settings import PLAYER_VELOCITY, SIN45, GREEN


class SmartBot(Creature):

    def __init__(self, bullet_sprites, enemies, client):
        super().__init__(color=GREEN)
        self.bullet_sprites = bullet_sprites
        self.enemies = enemies
        self.client = client

    def act(self, node_input):
        # self.print_surrounding_with_bullets()
        outputs = self.client.calculate(node_input)
        move_x = outputs[0]
        move_y = outputs[1]

        self.speed_x = 0
        self.speed_y = 0
        if move_x > 0.25:
            self.speed_x += PLAYER_VELOCITY
        elif move_x < -0.25:
            self.speed_y -= PLAYER_VELOCITY
        if move_y > 0.25:
            self.speed_y += PLAYER_VELOCITY
        elif move_y < -0.25:
            self.speed_y -= PLAYER_VELOCITY

        if self.speed_x and self.speed_y:
            self.speed_x *= SIN45
            self.speed_y *= SIN45


