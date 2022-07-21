from .nodes.client_node import ClientNode
from .nodes.travel_node import TravelNode


def create_client_nodes_list(number_of_clients_nodes: int):
    return [ClientNode(i, ) for i in range(number_of_clients_nodes)]


def create_travel_nodes_list(number_of_travel_nodes: int):
    return [TravelNode(i, 0 == i) for i in range(number_of_travel_nodes)]



class ProblemInstance:

    def __init__(self, number_of_client_nodes, number_of_travel_nodes, package_weights,distance_matrix):
        self.package_weights = package_weights
        self.client_nodes = create_client_nodes_list(number_of_client_nodes)
        self.travel_nodes = create_travel_nodes_list(number_of_travel_nodes)
        self.distanceMatrix = distance_matrix

    def get_client_nodes(self):
        return list.copy(self.client_nodes)

    def get_travel_nodes(self):
        return list.copy(self.travel_nodes)

    def get_single_client_node(self, index):
        return self.client_nodes[index]

    def get_single_travel_node(self, index):
        return self.travel_nodes[index]

    def get_distance_matrix(self):
        return self.distanceMatrix

    def get_distance(self, node1, node2):
        return self.distanceMatrix[node1][node2]