from config_files.neat_config import ACTIVATION_FUNCTION
from neat.calculations.connection import Connection


class Node:
    # like node_gene, but without redundant info for calculation like innov nums
    def __init__(self, x):
        self.x = x
        self.output = None
        self.connections = list()

    def calculate(self):
        input_sum = 0
        c: Connection
        for c in self.connections:
            if c.enabled:
                input_sum += c.weight * c.prev.output

        self.output = self.activation_function(input_sum)

    @staticmethod
    def activation_function(input_sum):
        return ACTIVATION_FUNCTION(input_sum)

    def __lt__(self, other):
        if type(other) != Node:
            raise TypeError
        return self.x < other.x

    def __eq__(self, other):
        if type(other) != Node:
            raise TypeError
        return self.x == other.x



