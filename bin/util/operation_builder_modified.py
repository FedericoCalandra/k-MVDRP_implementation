import math
from bin.nodes.client_node import ClientNode
from bin.nodes.node import Node
from bin.operations.flight import Flight
from bin.operations.operation import Operation
from bin.problem_instantiator import ProblemInstance


class OperationBuilder:
    def __init__(self, problem_instance: ProblemInstance, start_node: Node, end_node: Node,
                 number_of_clients_to_be_served: int, number_of_served_clients: int, visit_order: list[ClientNode]):
        self.problem_instance = problem_instance
        self.start_node = start_node
        self.end_node = end_node
        self.number_of_clients_to_be_served = number_of_clients_to_be_served
        self.number_of_served_clients = number_of_served_clients
        self.visit_order = visit_order.copy()

    def build_operation(self):
        # noinspection PyTypeChecker
        operation = Operation(self.problem_instance, self.start_node, self.end_node,
                              self.compute_flights_in_operation(), self.problem_instance.truck)
        return operation if operation.is_feasible() else None

    def compute_flights_in_operation(self):
        drone_assignments_list = self.compute_drone_assignments()
        flights = []
        clients_to_be_served = self.visit_order[self.number_of_served_clients:self.number_of_clients_to_be_served]
        pointer = 0
        for number_of_clients in drone_assignments_list:
            visited_clients = clients_to_be_served[pointer:(pointer + number_of_clients)]
            pointer += number_of_clients
            flights.append(Flight(self.start_node, self.end_node, visited_clients, self.problem_instance.drone))
        return flights

    # optimised assignments
    def compute_drone_assignments(self):
        n = self.number_of_clients_to_be_served - self.number_of_served_clients
        drone_assignments_list = []
        while n > 0:
            clients_visited_by_drone = math.ceil((self.number_of_clients_to_be_served - self.number_of_served_clients) /
                                                 self.problem_instance.number_of_available_drones)
            if clients_visited_by_drone < n:
                drone_assignments_list.append(clients_visited_by_drone)
                n -= clients_visited_by_drone
            else:
                drone_assignments_list.append(n)
                n = 0
        return drone_assignments_list
