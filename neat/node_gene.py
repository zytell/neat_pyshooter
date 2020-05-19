from neat.gene import Gene


class NodeGene(Gene):
    def __init__(self, innovation_num):
        super().__init__(innovation_num)
        self.x = 0
        self.y = 0

    def __hash__(self):
        return self.innovation_num

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.innovation_num == other.innovation_num




