from utils.data_structures.hashlist import HashList
from neat.connection_gene import ConnectionGene
from neat.node_gene import NodeGene
from random import random
from neat.calculations.calculator import Calculator
from config_files.neat_config import (
    c1, c2, c3,
    WEIGHT_RANDOM_STRENGTH, WEIGHT_SHIFT_STRENGTH,
    PROBABILITY_MUTATE_LINK, PROBABILITY_MUTATE_NODE, PROBABILITY_MUTATE_TOGGLE_LINK,
    PROBABILITY_MUTATE_WEIGHT_RANDOM, PROBABILITY_MUTATE_WEIGHT_SHIFT
)


class Genome:
    def __init__(self, neat):
        self.neat = neat
        self.connections = HashList()
        self.nodes = HashList()
        self.calculator = None

    def generate_calculator(self):
        self.calculator = Calculator(self)

    def calculate(self, lst):
        return self.calculator.calculate(lst)

    def distance(self, g2):
        g1 = self
        index_g1 = 0
        index_g2 = 0

        disjoint = 0
        # excess = 0 -- defined later
        weight_diff = 0
        similar = 0

        while index_g1 < len(g1.connections) and index_g2 < len(g2.connections):
            cg1: ConnectionGene = g1.connections[index_g1]
            cg2: ConnectionGene = g2.connections[index_g2]

            in1 = cg1.innovation_num
            in2 = cg2.innovation_num

            if in1 == in2:
                # similar gene
                similar += 1
                weight_diff += abs(cg1.weight - cg2.weight)

                index_g1 += 1
                index_g2 += 1
            elif in1 > in2:
                # disjoint gene of g2
                disjoint += 1
                index_g2 += 1
            else:
                # disjoint gene of g1
                disjoint += 1
                index_g1 += 1

        if similar != 0:
            weight_diff /= similar

        if len(g1.connections) > 0:
            g1_highest_innovation = g1.connections[-1].innovation_num
        else:
            g1_highest_innovation = 0

        if len(g2.connections) > 0:
            g2_highest_innovation = g2.connections[-1].innovation_num
        else:
            g2_highest_innovation = 0

        if g1_highest_innovation > g2_highest_innovation:  # g1 has higher innovation number
            excess = len(g1.connections) - index_g1
        else:
            excess = len(g2.connections) - index_g2  # g2 has higher innovation number

        N = max(len(g1.connections), len(g2.connections))
        if N < 20:
            N = 1

        return c1 * disjoint / N + c2 * excess / N + c3 * weight_diff

    @staticmethod
    def crossover(g1, g2, equal=False):
        # TODO: need to implement case of equal fitness.
        # assuming g1 has better fitness than g2.
        index_g1 = 0
        index_g2 = 0

        neat = g1.neat

        child = neat.get_empty_genome()

        while index_g1 < len(g1.connections) and index_g2 < len(g2.connections):
            cg1: ConnectionGene = g1.connections[index_g1]
            cg2: ConnectionGene = g2.connections[index_g2]

            in1 = cg1.innovation_num
            in2 = cg2.innovation_num

            if in1 > in2:  # disjoint gene of g2
                if equal:
                    child.connections.add(cg2.copy())
                index_g2 += 1

            elif in1 < in2:  # disjoint gene of g1
                child.connections.add(cg1.copy())
                index_g1 += 1

            else:  # in1 == in2, similar gene
                if random() > 0.5:
                    child.connections.add(cg1.copy())
                else:
                    child.connections.add(cg2.copy())

                index_g1 += 1
                index_g2 += 1

        while index_g1 < len(g1.connections):
            child.connections.add(g1.connections[index_g1].copy())
            index_g1 += 1

        if equal:
            while index_g2 < len(g2.connections):
                child.connections.add(g2.connections[index_g2].copy())
                index_g2 += 1

        c: ConnectionGene
        for c in child.connections.data:
            child.nodes.add(c.prev)
            child.nodes.add(c.next)

        return child

    def create_connection(self, id_node1, id_node2):
        cg = self.neat.get_connection(self.nodes[id_node1], self.nodes[id_node2])
        cg.weight = 0.4
        if cg not in self.connections:
            self.connections.sorted_add(cg)

    def mutate_random(self):
        if PROBABILITY_MUTATE_TOGGLE_LINK > random():
            self.mutate_link_toggle()

        if PROBABILITY_MUTATE_LINK > random():
            self.mutate_link()

        if PROBABILITY_MUTATE_NODE > random():
            self.mutate_node()

        if PROBABILITY_MUTATE_WEIGHT_SHIFT > random():
            self.mutate_weight_random()

        if PROBABILITY_MUTATE_WEIGHT_RANDOM > random():
            self.mutate_weight_random()

    def mutate_link(self):
        for i in range(100):

            a: NodeGene = self.nodes.select_random()
            b: NodeGene = self.nodes.select_random()

            if a.x == b.x:
                continue

            if a.x < b.x:
                con = ConnectionGene(a, b)  # creates connection without innovation number
            else:
                con = ConnectionGene(b, a)  # same, avoids recursion.

            if con in self.connections:  # if it already exists:
                continue  # discards con, creates new one. (further code gets disused).

            # con is not already in global db (neat):
            con = self.neat.get_connection(con.prev, con.next)  # adds con to db and assigns innov number
            con.weight = (random() * 2 - 1) * WEIGHT_RANDOM_STRENGTH
            self.connections.sorted_add(con)  # adds con to local (genome) db
            return  # found con, end loop.

    def mutate_node(self):
        con: ConnectionGene
        con = self.connections.select_random()
        if not con or not con.enabled:
            return

        prev: NodeGene = con.prev
        next: NodeGene = con.next

        replace_index = self.neat.get_replace_index(prev, next)

        if replace_index == 0:
            middle: NodeGene = self.neat.get_new_node()
            middle.x = (prev.x + next.x) / 2
            middle.y = (prev.y + next.y) / 2 + random() * 0.2 - 0.1  # added random for better visual repr.
            self.neat.set_replace_index(prev, next, middle.innovation_num)
        else:
            middle = self.neat.get_node(replace_index)

        con1: ConnectionGene = self.neat.get_connection(prev, middle)
        con2: ConnectionGene = self.neat.get_connection(middle, next)

        con1.weight = 1
        con2.weight = con.weight
        con2.enabled = con.enabled

        con.enabled = False
        if con1.innovation_num is None:
            raise Exception('no innovation number')
        if con2.innovation_num is None:
            raise Exception('no innovation number')
        self.connections.sorted_add(con1)
        self.connections.sorted_add(con2)

        self.nodes.add(middle)

    def mutate_weight_shift(self):
        con: ConnectionGene = self.connections.select_random()
        if con:
            con.weight += (random() * 2 - 1) * WEIGHT_SHIFT_STRENGTH

    def mutate_weight_random(self):
        con: ConnectionGene = self.connections.select_random()
        if con:
            con.weight = (random() * 2 - 1) * WEIGHT_RANDOM_STRENGTH

    def mutate_link_toggle(self):
        con: ConnectionGene = self.connections.select_random()
        if con:
            con.toggle_enabled()
