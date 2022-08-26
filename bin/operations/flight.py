from bin.nodes.client_node import ClientNode
from bin.nodes.node import Node
from bin.operations.movement import Movement
from bin.problem_instantiator import ProblemInstance
from bin.veicles.drone import Drone


class Flight:
    def __init__(self, takeoff_node: Node, landing_node: Node,
                 visited_clients: list[ClientNode], drone: Drone):
        self.takeoff_node = takeoff_node
        self.landing_node = landing_node
        self.visited_clients = visited_clients
        self.drone = drone
        self.total_weight = self.compute_total_weight()
        self.list_of_movements = self.compute_movements()

    def compute_movements(self):
        if self.visited_clients:
            movements = [Movement(self.takeoff_node, self.visited_clients[0], self.drone)]
            for i in range(1, len(self.visited_clients)):
                movements.append(Movement(self.visited_clients[i - 1], self.visited_clients[i], self.drone))
            movements.append(
                Movement(self.visited_clients[len(self.visited_clients) - 1], self.landing_node, self.drone))
            return movements

    def compute_total_weight(self):
        total_weight = 0
        for c in self.visited_clients:
            total_weight += c.weight
        return total_weight

    def _compute_weight_associated_to_movement(self, movement):
        weight_delivered = 0
        for move in self.list_of_movements:
            if movement == move:
                break
            for client in self.visited_clients:
                if move.end_node == client:
                    weight_delivered += client.weight
        return self.total_weight - weight_delivered

    def clone(self):
        return Flight(self.takeoff_node, self.landing_node, self.visited_clients, self.drone)

    def __str__(self):
        str_visited_clients = ""
        for client in self.visited_clients:
            str_visited_clients += str(client) + ","
        return "[" + str(self.takeoff_node) + ", " + str_visited_clients + " " + str(self.landing_node) + "]"

    def __copy__(self):
        return Flight(self.takeoff_node, self.landing_node, self.visited_clients.copy(), self.drone)

    def compute_energy_used_for_flight(self, problem_instance: ProblemInstance):
        energy_used = 0
        # noinspection PyTypeChecker
        time_for_truck_movement = Movement(self.takeoff_node, self.landing_node, problem_instance.
                                           truck).compute_movement_time(problem_instance.
                                                                        compute_distance_for_truck(self.takeoff_node,
                                                                                                   self.landing_node))
        drone_flight_time = self.compute_flight_time(problem_instance)
        if self.list_of_movements:
            for movement in self.list_of_movements:
                energy_used += self.drone.get_energy_used(movement.compute_movement_time(
                    problem_instance.compute_distance_for_drone(
                        movement.start_node, movement.end_node)), self._compute_weight_associated_to_movement(movement))
        if drone_flight_time < time_for_truck_movement:
            energy_used += self.drone.get_hov_energy_used(time_for_truck_movement - drone_flight_time)
        return energy_used

    def compute_flight_time(self, problem_instance: ProblemInstance):
        flight_time = 0
        if self.list_of_movements:
            for movement in self.list_of_movements:
                flight_time += movement.compute_movement_time(
                    problem_instance.compute_distance_for_drone(movement.start_node, movement.end_node))
        return flight_time
