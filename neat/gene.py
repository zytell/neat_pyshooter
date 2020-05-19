

class Gene:
    def __init__(self, innovation_num=None):
        self.innovation_num = innovation_num

    def __lt__(self, other):
        return self.innovation_num < other.innovation_num

