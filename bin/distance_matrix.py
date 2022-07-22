from bin.nodes.node import Node
from bin.nodes.travel_node import TravelNode
from bin.problem_instantiator import ProblemInstance


class DistanceMatrix:
    def __init__(self, matrix_of_distances, problem_instance: ProblemInstance):
        self._distance_matrix = matrix_of_distances
        self.problem_instance = problem_instance

    def get_distance(self, node1: Node, node2: Node):
        node1_index = node1.index
        node2_index = node2.index

        if type(node1) is TravelNode:
            node1_index = node1.index + self.problem_instance.get_number_of_clients()
        if type(node2) is TravelNode:
            node2_index = node2.index + self.problem_instance.get_number_of_clients()

        return self._distance_matrix[node1_index][node2_index]
