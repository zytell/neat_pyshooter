from utils.data_structures.hashlist import HashList
from neat.node_gene import NodeGene
from neat.genome import Genome
from neat.connection_gene import ConnectionGene
from neat.neat_visual.visual import Visual
from neat.client import Client
from neat.species import Species
from utils.data_structures.random_selector import RandomSelector
from random import random
from config_files.neat_config import (
    SURVIVORS,
    OUTPUT_SIZE, MAX_CLIENTS, GENERATIONS)

empty_genome = False


class Neat:
    def __init__(self, input_size, output_size, max_clients):
        self.input_size = input_size
        self.output_size = output_size
        self.max_clients = max_clients
        self.all_connections = dict()  # {Connection Gene : Connection Gene}
        self.all_nodes = HashList()

        self.clients = HashList()
        self.species = HashList()

        for i in range(input_size):
            n = self.get_new_node()
            n.x = 0.1
            n.y = (i + 1) / (input_size + 1)
            self.all_nodes.add(n)

        for i in range(output_size):
            n = self.get_new_node()
            n.x = 0.9
            n.y = (i + 1) / (output_size + 1)
            self.all_nodes.add(n)

        for i in range(self.max_clients):
            c = Client()
            c.genome = self.get_empty_genome()
            self.clients.add(c)

    def set_replace_index(self, node1: NodeGene, node2: NodeGene, index):
        if ConnectionGene(node1, node2) not in self.all_connections.keys():
            raise Exception("error, cg doesn't already exit")
        self.all_connections[ConnectionGene(node1, node2)].replace_index = index

    def get_replace_index(self, node1, node2):
        con = ConnectionGene(node1, node2)
        data = self.all_connections[con]
        if data.replace_index is None:
            return 0
        return data.replace_index

    def get_client(self, index):
        return self.clients[index]

    def get_connection(self, node1, node2):
        cg = ConnectionGene(node1, node2)

        if cg in self.all_connections.keys():
            cg.innovation_num = self.all_connections[cg].innovation_num
        else:
            innov_num = len(self.all_connections) + 1
            cg.innovation_num = innov_num
            self.all_connections[cg] = cg
        return cg

    def get_empty_genome(self):
        g: Genome = Genome(self)
        for i in range(self.input_size + self.output_size):
            g.nodes.add(self.get_node(i + 1))
        return g

    def get_new_node(self):
        n = NodeGene(len(self.all_nodes) + 1)
        self.all_nodes.add(n)
        return n

    def get_node(self, id: int):
        if 0 <= id <= len(self.all_nodes):
            return self.all_nodes[id - 1]
        return self.get_new_node()

    def evolve(self):
        self.gen_species()
        self.kill()
        self.remove_extinct_species()
        self.reproduce()
        self.mutate()

        c: Client
        for c in self.clients.data:
            c.generate_calculator()

    def gen_species(self):
        s: Species
        for s in self.species.data:
            s.reset()

        c: Client
        for c in self.clients.data:
            if c.species:
                continue

            found = False
            for s in self.species.data:
                if s.put(c):  # successfully found matching species
                    found = True
                    break

            if not found:
                self.species.add(Species(c))

        for s in self.species.data:
            s.evaluate_score()

    def kill(self):
        s: Species
        for s in self.species.data:
            s.kill(1 - SURVIVORS)

    def remove_extinct_species(self):
        for i in range(len(self.species))[::-1]:
            if len(self.species.data[i]) <= 1:
                self.species[i].go_extinct()
                self.species.pop(i)

    def reproduce(self):
        selector = RandomSelector()
        s: Species
        if len(self.species.data) is 0:
            self.gen_species()
        for s in self.species.data:
            selector.add(s, s.score)

        c: Client
        for c in self.clients.data:
            if not c.species:
                s = selector.random()
                c.genome = s.breed()
                s.force_put(c)

    def mutate(self):
        c: Client
        for c in self.clients.data:
            c.mutate()

    def print_species(self, generation=None):

        if generation is not None:
            print('# --------- GENERATION %s --------- #' % (generation + 1))
        else:
            print('# --------------------------------- #')
        s: Species
        for s in self.species.data:
            print([cg.innovation_num for cg in s.clients.data[-1].genome.connections if cg.enabled], round(s.score, 2), len(s))

    @staticmethod
    def print_details(best_client):
        print('\n# -----------FINISHED----------- #')
        print('DATA: innovation nums of one client, avg score, num of clients')
        print('BEST CLIENT SCORE:', best_client.score)


def main():
    input_size = 10
    n = Neat(input_size=input_size, output_size=OUTPUT_SIZE, max_clients=MAX_CLIENTS)
    # empty_genome = True
    if empty_genome:
        g = n.get_empty_genome()
        Visual(g)

    inputs = list()
    for _ in range(input_size):
        inputs.append(random())

    for i in range(GENERATIONS):
        c: Client
        for c in n.clients.data:
            score = c.calculate(inputs)[0]
            c.score = score

        n.evolve()
        n.print_species(i)

    best_client = max(n.clients, key=lambda x: x.score)
    n.print_details(best_client)

    Visual(best_client.genome)


if __name__ == '__main__':
    main()
