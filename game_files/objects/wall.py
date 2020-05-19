from game_files.objects.game_object import GameObject


class Wall(GameObject):
    def __init__(self, start_loc=(200, 300), size=(50, 50), bottomright=False, topleft=False):
        super().__init__(start_loc=start_loc, size=size, bottomright=bottomright, topleft=topleft)
