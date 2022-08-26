import unittest
import numpy as np
from bin import problem_instantiator
from bin.nodes.node import Node
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


class ProblemInstanceTestSuite(unittest.TestCase):
    def setUp(self):

        class Exp(EnergyFunction):
            def apply(self, flight_time, carried_weight, is_hovering: bool):
                if is_hovering:
                    return 1 * flight_time
                return 1 * flight_time * carried_weight

        self.truck_distance_matrix = np.ones([10, 10])
        self.num_of_clients = 6
        self.num_of_travels = 4
        self.package_weights = [1, 1, 2, 1, 1, 3]
        self.drone_distance_matrix = np.ones([10, 10])
        self.drone = Drone(1.0, 10, 1, Exp())
        self.truck = Truck(10)
        self.problem_instance = problem_instantiator.ProblemInstance(self.num_of_clients, self.num_of_travels,
                                                                     self.package_weights, self.drone_distance_matrix,
                                                                     self.truck_distance_matrix, 1, self.drone,
                                                                     self.truck)

    def test_instanceProblem_getters(self):
        for i in range(len(self.problem_instance.client_nodes)):
            self.assertEqual(self.problem_instance.client_nodes[i].index, i)
            self.assertEqual(self.problem_instance.client_nodes[i].weight, self.package_weights[i])

        for i in range(len(self.problem_instance.travel_nodes)):
            self.assertEqual(self.problem_instance.travel_nodes[i].index, i)
            self.assertEqual(self.problem_instance.travel_nodes[i].is_warehouse, i == 0)

        nodes = list.copy(self.problem_instance.client_nodes)
        nodes.extend(self.problem_instance.travel_nodes)

        for i in range(len(self.problem_instance.drone_distance_matrix.get_matrix())):
            for j in range(len(self.problem_instance.drone_distance_matrix.get_matrix()[i])):
                self.assertEqual(self.problem_instance.compute_distance_for_drone(nodes[i], nodes[j]),
                                 self.drone_distance_matrix[i][j])
    def test_compute_distance(self):
        node_1 = self.problem_instance.get_single_travel_node(0)
        node_2 = self.problem_instance.get_single_client_node(0)
        self.assertEqual(self.problem_instance.compute_distance_for_drone(node_1, node_2),
                         self.drone_distance_matrix[self.num_of_clients][0])
if __name__ == '__main__':
    unittest.main()




















