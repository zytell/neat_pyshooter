from neat.calculations.calculator import Calculator


class Client:
    def __init__(self):
        self.calculator = None

        self.genome = None
        self.score = None
        self.species = None

    def generate_calculator(self):
        self.calculator = Calculator(self.genome)

    def calculate(self, node_input):
        if not self.calculator:
            self.generate_calculator()
        return self.calculator.calculate(node_input)

    def distance(self, other):
        return self.genome.distance(other.genome)

    def mutate(self):
        self.genome.mutate_random()
