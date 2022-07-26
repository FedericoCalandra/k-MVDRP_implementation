from bin.distance_matrix.distance_matrix import DistanceMatrix
from .nodes.node import Node
from .nodes.client_node import ClientNode
from .nodes.travel_node import TravelNode
from .veicles.drone import Drone
from .veicles.truck import Truck


def create_client_nodes_list(client_nodes_coordinates: list[list[float]], package_weights):
    return [ClientNode(i, client_nodes_coordinates[i][0], client_nodes_coordinates[i][1], package_weights[i])
            for i in range(len(client_nodes_coordinates))]


def create_travel_nodes_list(travel_nodes_coordinates: list[list[float]]):
    return [TravelNode(i, travel_nodes_coordinates[i][0], travel_nodes_coordinates[i][1], 0 == i)
            for i in range(len(travel_nodes_coordinates))]


class ProblemInstance:

    def __init__(self, client_nodes_coordinates, travel_nodes_coordinates, list_of_package_weights,
                 drone_distance_matrix: DistanceMatrix, truck_distance_matrix: DistanceMatrix,
                 number_of_available_drones, drone_type: Drone,
                 truck_type: Truck):

        self.list_of_package_weights = list_of_package_weights
        self.client_nodes = create_client_nodes_list(client_nodes_coordinates, list_of_package_weights)
        self.travel_nodes = create_travel_nodes_list(travel_nodes_coordinates)
        self.drone_distance_matrix = drone_distance_matrix
        self.truck_distance_matrix = truck_distance_matrix
        self.number_of_available_drones = number_of_available_drones
        self.drone = drone_type
        self.truck = truck_type

    def get_list_of_client_nodes(self):
        return list.copy(self.client_nodes)

    def get_list_of_travel_nodes(self):
        return list.copy(self.travel_nodes)

    def get_single_client_node(self, index):
        return self.client_nodes[index]

    def get_single_travel_node(self, index):
        return self.travel_nodes[index]

    def compute_distance_for_drone(self, node1: Node, node2: Node):
        node1_index = node1.index
        node2_index = node2.index
        if type(node1) is TravelNode:
            node1_index = node1.index + self.get_number_of_clients()
        if type(node2) is TravelNode:
            node2_index = node2.index + self.get_number_of_clients()
        return self.drone_distance_matrix.get_matrix()[node1_index][node2_index]

    def compute_distance_for_truck(self, node1: TravelNode, node2: TravelNode):
        node1_index = node1.index
        node2_index = node2.index
        return self.truck_distance_matrix.get_matrix()[node1_index][node2_index]

    def get_number_of_clients(self):
        return len(self.client_nodes)

    def get_number_of_travel_nodes(self):
        return len(self.travel_nodes)

    def add_client_node(self, x_coordinate, y_coordinate, weight):
        self.client_nodes.append(ClientNode(len(self.client_nodes), x_coordinate, y_coordinate, weight))

    def add_travel_node(self, x_coordinate, y_coordinate):
        self.travel_nodes.append(TravelNode(len(self.travel_nodes), x_coordinate, y_coordinate, False))

    def set_warehouse(self, index):
        for tn in self.travel_nodes:
            if tn.is_warehouse:
                tn.is_warehouse = False
        self.travel_nodes[index].is_warehouse = True

    def get_warehouse(self):
        warehouse = None
        for t in self.travel_nodes:
            if t.is_warehouse:
                warehouse = t
                break
        return warehouse
