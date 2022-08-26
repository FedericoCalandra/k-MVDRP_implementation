import bin.operations.flight
from bin.operations.flight import Flight
from bin.operations.movement import Movement
from bin.operations.operation import Operation
from bin.problem_instantiator import ProblemInstance
import itertools


class BasicSolver:

    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance
        self.feasible_flights = []
        self.all_feasible_operations = []

    def compute_all_feasible_truck_movements(self):
        all_feasible_truck_movements = []
        for start_node in self.problem_instance.travel_nodes:
            for end_node in self.problem_instance.travel_nodes:
                all_feasible_truck_movements.append(Movement(start_node, end_node, self.problem_instance.truck))
        return all_feasible_truck_movements

    def compute_all_feasible_operations(self):
        pointer = 0
        ops = []
        for movement in self.compute_all_feasible_truck_movements():
            self.compute_flights(Flight(movement.start_node, movement.end_node, [], self.problem_instance.drone))
            flights = []
            for i in range(pointer, len(self.feasible_flights)):
                flights.append(self.feasible_flights[i])
            combinations = itertools.combinations(flights, self.problem_instance.number_of_available_drones)
            for flights_comb in combinations:
                # noinspection PyTypeChecker
                ops.append(Operation(movement.start_node, movement.end_node, flights_comb, self.problem_instance.truck))

            # C'E' UN PROBLEMA!!!
            pointer = len(self.feasible_flights) - pointer
            for operation in ops:
                self.all_feasible_operations.append(operation)
        return self.all_feasible_operations

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
                if flight.compute_energy_used_for_flight(self.problem_instance) < self.problem_instance.\
                        drone.max_energy_available:
                    possible_flights.append(new_flight)
        return possible_flights
