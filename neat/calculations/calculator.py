from neat.calculations.node import Node
from neat.calculations.connection import Connection
from utils.data_structures.hashlist import HashList


class Calculator:
    def __init__(self, g):
        self.input_nodes = list()
        self.hidden_nodes = list()
        self.output_nodes = list()

        node_genes: HashList = g.nodes
        connection_genes: HashList = g.connections

        node_dict = dict()

        for node_gene in node_genes.data:
            new_node = Node(node_gene.x)
            node_dict[node_gene.innovation_num] = new_node

            if node_gene.x <= 0.1:
                self.input_nodes.append(new_node)
            elif node_gene.x >= 0.9:
                self.output_nodes.append(new_node)
            else:
                self.hidden_nodes.append(new_node)

        self.hidden_nodes.sort(key=lambda n: n.x)

        for connection_gene in connection_genes:
            prev_node_gene = connection_gene.prev
            next_node_gene = connection_gene.next

            prev_node = node_dict[prev_node_gene.innovation_num]
            next_node = node_dict[next_node_gene.innovation_num]

            con = Connection(prev_node, next_node)
            con.weight = connection_gene.weight
            con.enabled = connection_gene.enabled

            next_node.connections.append(con)

    def calculate(self, node_input):
        if len(self.input_nodes) != len(node_input):
            raise Exception(node_input)
        for i, node in enumerate(self.input_nodes):
            node.output = node_input[i]

        for n in self.hidden_nodes:
            n.calculate()

        output = list()
        for i, output_node in enumerate(self.output_nodes):
            output_node.calculate()
            output.append(output_node.output)

        return output

