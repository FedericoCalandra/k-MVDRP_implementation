import unittest
import numpy as np

from bin import problem_instantiator
from bin.nodes.travel_node import TravelNode
from bin.operations.travel import TruckTravel
from bin.veicles.truck import Truck


class OperationsTestSuite(unittest.TestCase):

    def test_truck_travel(self):
        num_of_clients = 6
        num_of_travels = 4
        package_weights = [1, 1, 2, 1, 1, 3]
        distance_matrix = np.ones([10, 10])
        problem_instance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels,
                                                                package_weights, distance_matrix, 1)

        truck = Truck(10)
        travel = TruckTravel(problem_instance, problem_instance.get_single_travel_node(0),
                             problem_instance.get_single_travel_node(1), truck)
        time = travel.compute_travel_time()
        print("travel time computed: " + str(time))

        self.assertEqual(time, distance_matrix[num_of_clients][num_of_clients + 1] / truck.speed)
