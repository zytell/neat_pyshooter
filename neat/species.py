from utils.data_structures.hashlist import HashList
from neat.genome import Genome
from config_files.neat_config import (
    CP
)


class Species:
    def __init__(self, representative):
        self.clients = HashList()
        self.representative = representative
        self.representative.species = self
        self.clients.add(representative)
        self.score = None

    def put(self, client):
        if client.distance(self.representative) < CP:
            client.species = self
            self.clients.add(client)
            return True
        return False

    def force_put(self, client):
        client.species = self
        self.clients.add(client)

    def go_extinct(self):
        for c in self.clients.data:
            c.species = None

    def evaluate_score(self):
        v = 0
        for c in self.clients.data:
            v += c.score
        self.score = v / len(self.clients)

    def reset(self):
        representative = self.clients.select_random()
        for c in self.clients.data:
            c.species = None
        self.clients.__init__()

        self.clients.add(representative)
        representative.species = self
        self.score = 0

    def kill(self, percentage):
        # sorts that the weakest are first
        self.clients.data.sort(key=lambda x: x.score)

        amount = int(percentage * len(self.clients))  # so amount wont change when loop runs.
        for _ in range(amount):
            self.clients.pop(0).species = None  # always removes the first - weakest client.

    def breed(self):
        c1 = self.clients.select_random()
        c2 = self.clients.select_random()

        if c1.score > c2.score:
            return Genome.crossover(c1.genome, c2.genome)
        elif c1.score < c2.score:
            return Genome.crossover(c2.genome, c1.genome)
        else:
            return Genome.crossover(c1.genome, c2.genome, equal=True)

    def __len__(self):
        return len(self.clients)
