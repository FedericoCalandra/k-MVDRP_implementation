from .distance_matrix import DistanceMatrix
from .nodes.client_node import ClientNode
from .nodes.travel_node import TravelNode


def create_client_nodes_list(number_of_clients_nodes: int, package_weights):
    return [ClientNode(i, package_weights[i]) for i in range(number_of_clients_nodes)]


def create_travel_nodes_list(number_of_travel_nodes: int):
    return [TravelNode(i, 0 == i) for i in range(number_of_travel_nodes)]


class ProblemInstance:

    def __init__(self, number_of_client_nodes, number_of_travel_nodes, package_weights,
                 distance_matrix, number_of_drones):

        self.package_weights = package_weights
        self.client_nodes = create_client_nodes_list(number_of_client_nodes, package_weights)
        self.travel_nodes = create_travel_nodes_list(number_of_travel_nodes)
        self.distance_matrix = DistanceMatrix(distance_matrix, self)
        self.number_of_drones = number_of_drones

    def get_copy_of_client_nodes(self):
        return list.copy(self.client_nodes)

    def get_copy_of_travel_nodes(self):
        return list.copy(self.travel_nodes)

    def get_single_client_node(self, index):
        return self.client_nodes[index]

    def get_single_travel_node(self, index):
        return self.travel_nodes[index]

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_number_of_clients(self):
        return len(self.client_nodes)

    def get_number_of_travel_nodes(self):
        return len(self.travel_nodes)

    def add_client_node(self, index, weight):
        self.client_nodes.insert(index, ClientNode(index, weight))

    def add_travel_node(self, index):
        self.travel_nodes.insert(index, TravelNode(index, False))

    def set_warehouse(self, index):
        for tn in self.travel_nodes:
            if tn.is_warehouse:
                tn.is_warehouse = False
        self.travel_nodes[index].is_warehouse = True
