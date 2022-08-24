import bin.operations.flight
from bin.operations.flight import Flight
from bin.operations.movement import Movement
from bin.problem_instantiator import ProblemInstance
import itertools


def get_combinations(array):
    combinations = []
    for number_of_elements in range(1, len(array) + 1):
        for subset in itertools.combinations(array, number_of_elements):
            combinations.append(subset)
    return combinations


class BasicSolver:

    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance
        self.feasible_flights = []
        #self.all_feasible_operations = self.compute_all_feasible_operations()

    def compute_all_feasible_truck_movements(self):
        all_feasible_truck_movements = []
        for start_node in self.problem_instance.travel_nodes:
            for end_node in self.problem_instance.travel_nodes:
                all_feasible_truck_movements.append(Movement(start_node, end_node, self.problem_instance.truck))
        return all_feasible_truck_movements

    def compute_all_feasible_flights(self):         #potrei calcolare direttamente le operazioni
        for movement in self.compute_all_feasible_truck_movements():
            self.compute_flights(Flight(movement.start_node, movement.end_node, [], self.problem_instance.drone))
        return self.feasible_flights

    def compute_flights(self, flight):
        computed_flights = self.compute_feasible_steps(flight)
        if computed_flights:
            for flight in computed_flights:
                self.feasible_flights.append(flight)
                self.compute_flights(flight)

    def compute_feasible_steps(self, flight):
        possible_flights = []
        for client in self.problem_instance.client_nodes:
            new_flight = flight.__copy__()
            if client not in new_flight.visited_clients:
                new_flight.visited_clients.insert(len(new_flight.visited_clients) - 1, client)
                if self.energy_used_for_flight(new_flight) < self.problem_instance.drone.max_energy_available:
                    possible_flights.append(new_flight)
        return possible_flights


    def energy_used_for_flight(self, flight):
        energy_used = 0
        flight_time = flight.compute_flight_time(self.problem_instance)
        energy_used = flight.drone.get_energy_used()
        truck_time = Movement(flight.takeoff_node, flight.landing_node,
                              self.problem_instance.truck).compute_movement_time()
        return 1


    def compute_all_feasible_operations(self):
        operations_computed = []
        for nodes in self.all_feasible_truck_movements:
            operations_computed.append(get_combinations(self.get_subset_of_feasible_flight(nodes[0], nodes[1])))
        return operations_computed

    def get_subset_of_feasible_flight(self, start_node, end_node):
        set_to_be_returned = []
        for flight in self.compute_all_feasible_flights():
            if flight[0] == start_node and flight[len(flight) - 1] == end_node:
                set_to_be_returned.append(flight)
        return set_to_be_returned
