from neat.gene import Gene
from neat.node_gene import NodeGene
from config_files.neat_config import (
    MAX_NODES
)


class ConnectionGene(Gene):
    def __init__(self, prev, next):
        super().__init__()
        self.prev: NodeGene = prev
        self.next: NodeGene = next

        self.weight = 1.0
        self.enabled = True

        self.replace_index = None

    def __eq__(self, other):
        if type(other) != ConnectionGene:
            return False
        return self.prev == other.prev and self.next == other.next

    def __hash__(self):
        return MAX_NODES * self.prev.innovation_num + self.next.innovation_num

    def copy(self):
        cg = ConnectionGene(self.prev, self.next)
        cg.weight = self.weight
        cg.enabled = cg.enabled
        cg.innovation_num = self.innovation_num
        cg.replace_index = self.replace_index
        return cg

    def toggle_enabled(self):
        self.enabled = not self.enabled


def main():
    c1 = ConnectionGene(NodeGene(2), NodeGene(3))
    c2 = ConnectionGene(NodeGene(2), NodeGene(4))
    c1.innovation_num = 2
    c2.innovation_num = 2

    print(hash(c1))

    lst = [c1, 2]

    print(c1 in lst)
    print(c1 == c2)


if __name__ == '__main__':
    main()




