import unittest
import numpy as np
from bin import problem_instantiator
from bin.operations.flight import Flight
from bin.operations.operation import Operation
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


class OperationsTestSuite(unittest.TestCase):

    def test_truck_travel(self):

        class Exp(EnergyFunction):
            def apply(self, flight_time, carried_weight, is_hovering: bool):
                if is_hovering:
                    return 1 * flight_time
                return 1 * flight_time * carried_weight

        drone = Drone(1.0, 10, 10.3, Exp())
        truck = Truck(1.0)
        package_weights = [1, 1, 2, 1, 1, 3]
        drone_distance_matrix = [[0, 7, 10, 5, 5.4, 12],
                                 [7, 0, 7, 5, 3, 8.6],
                                 [10, 7, 0, 11.1, 5.4, 2],
                                 [5, 5, 11.1, 0, 5.8, 13],
                                 [5.4, 3, 5.4, 5.8, 0, 7.3],
                                 [12, 8.6, 2, 13, 7.3, 0]]
        truck_distance_matrix = [[0, 5.8, 13],
                                 [5.8, 0, 7.3],
                                 [13, 7.3, 0]]
        num_of_clients = len(drone_distance_matrix) - len(truck_distance_matrix)
        num_of_travels = len(truck_distance_matrix)

        problem_instance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels,
                                                                package_weights, drone_distance_matrix,
                                                                truck_distance_matrix, 1, drone, truck)

        flight = Flight(problem_instance.get_single_travel_node(0), problem_instance.get_single_travel_node(1),
                        [problem_instance.client_nodes[0]], drone)

        operation = Operation(problem_instance, problem_instance.get_single_travel_node(0),
                              problem_instance.get_single_travel_node(1), [flight], truck)

        print("is_feasible = " + str(operation.is_feasible()))
        print("operation_time = " + str(operation.compute_operation_time()))
        print(flight)
        print("energy: " + str(flight.compute_energy_used_for_flight(problem_instance)))
        self.assertEqual(operation.compute_operation_time(), 10.4)
        self.assertEqual(operation.is_feasible(), True)
