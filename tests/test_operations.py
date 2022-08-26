import unittest
import numpy as np
from bin import problem_instantiator
from bin.nodes.travel_node import TravelNode
from bin.operations.travel import TruckTravel
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

        num_of_clients_node = 2
        num_of_travels_node = 2
        package_weights = [2, 2]
        length = num_of_clients_node + num_of_travels_node
        drone = Drone(3.0, 10, 1, Exp())
        truck = Truck(0.4)
        drone_distance_matrix = np.ones([length, length]) * 2
        truck_distance_matrix = np.ones([length, length])

        problem_instance = problem_instantiator.ProblemInstance(num_of_clients_node, num_of_travels_node,
                                                                package_weights, drone_distance_matrix,
                                                                truck_distance_matrix, 3, drone, truck)

        travel = TruckTravel(problem_instance, problem_instance.get_single_travel_node(0),
                             problem_instance.get_single_travel_node(1), truck)
        time = travel.compute_travel_time()
        print("travel time computed: " + str(time))

        self.assertEqual(time, drone_distance_matrix[num_of_clients_node][num_of_clients_node + 1] / truck.speed)
