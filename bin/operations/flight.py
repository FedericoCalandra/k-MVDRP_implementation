from bin.nodes.client_node import ClientNode
from bin.nodes.travel_node import TravelNode
from bin.operations.movement import Movement
from bin.problem_instantiator import ProblemInstance
from bin.veicles.drone import Drone


class Flight:
    def __init__(self, problem_instance: ProblemInstance, takeoff_node: TravelNode, landing_node: TravelNode,
                 visited_clients: list[ClientNode], drone: Drone):
        self.problem_instance = problem_instance
        self.takeoff_node = takeoff_node
        self.landing_node = landing_node
        self.visited_clients = visited_clients
        self.drone = drone
        self.total_weight = self.compute_total_weight()
        self.set_of_movements = self.compute_movements()

    def compute_movements(self):
        movements = [Movement(self.takeoff_node, self.visited_clients[0], self.drone)]
        for i in range(1, len(self.visited_clients)):
            movements.append(Movement(self.visited_clients[i - 1], self.visited_clients[i], self.drone))
        movements.append(Movement(self.visited_clients[len(self.visited_clients) - 1], self.landing_node, self.drone))
        return movements

    def compute_total_weight(self):
        total_weight = 0
        for c in self.visited_clients:
            total_weight += c.weight
        return total_weight

    def compute_flight_time(self):
        flight_time = 0
        for movement in self.set_of_movements:
            flight_time += movement.compute_movement_time(self.problem_instance
                                                          .get_distance(movement.start_node, movement.end_node))
        return flight_time
