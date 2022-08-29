from bin.nodes.travel_node import TravelNode
from bin.operations.flight import Flight
from bin.operations.movement import Movement
from bin.problem_instantiator import ProblemInstance
from bin.veicles.truck import Truck


class Operation:
    def __init__(self, problem_instance: ProblemInstance, start_node: TravelNode, end_node: TravelNode,
                 flights: list[Flight], truck: Truck):
        self.problem_instance = problem_instance
        self.start_node = start_node
        self.end_node = end_node
        self.flights = flights
        self.truck_movement = Movement(start_node, end_node, truck)

    def __str__(self):
        str_flights = ""
        for flight in self.flights:
            str_flights += str(flight) + "\n"
        return "Truck: " + str(self.truck_movement) + "\nDrone flights:\n" + str_flights

    def is_feasible(self):
        is_feasible = True
        if self.flights:
            for flight in self.flights:
                if flight.compute_energy_used_for_flight(self.problem_instance) > \
                        self.problem_instance.drone.max_energy_available:
                    is_feasible = False
                    break
        return is_feasible

    def compute_operation_time(self):
        drone_times = []
        for flight in self.flights:
            drone_times.append(flight.compute_flight_time(self.problem_instance))
        max_drone_time = max(drone_times)
        truck_time = self.truck_movement.compute_movement_time(
            self.problem_instance.compute_distance_for_truck(self.start_node, self.end_node))
        return max(truck_time, max_drone_time)
