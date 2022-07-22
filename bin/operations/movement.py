from bin.nodes.node import Node
from bin.veicles.generic_veicle import Veicle


class Movement:
    def __init__(self, start_node: Node, end_node: Node, veicle: Veicle):
        self.start_node = start_node
        self.end_node = end_node
        self.veicle = veicle

    def compute_movement_time(self, distance_between_nodes):
        return distance_between_nodes / self.veicle.speed
