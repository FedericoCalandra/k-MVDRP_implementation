import unittest
import numpy as np
from bin import problem_instantiator
from bin.nodes.node import Node


class ProblemInstanceTestSuite(unittest.TestCase):

    def test_instanceProblem_getters(self):
        num_of_clients = 6
        num_of_travels = 4
        package_weights = [1, 1, 2, 1, 1, 3]
        distance_matrix = np.ones([10, 10])
        problem_instance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels,
                                                                package_weights, distance_matrix, 1)

        for i in range(len(problem_instance.client_nodes)):
            self.assertEqual(problem_instance.client_nodes[i].index, i)
            self.assertEqual(problem_instance.client_nodes[i].weight, package_weights[i])

        for i in range(len(problem_instance.travel_nodes)):
            self.assertEqual(problem_instance.travel_nodes[i].index, i)
            self.assertEqual(problem_instance.travel_nodes[i].is_warehouse, i == 0)

        nodes = list.copy(problem_instance.client_nodes)
        nodes.extend(problem_instance.travel_nodes)

        for i in range(len(problem_instance.distance_matrix.get_matrix())):
            for j in range(len(problem_instance.distance_matrix.get_matrix()[i])):
                self.assertEqual(problem_instance.compute_distance(nodes[i], nodes[j]), distance_matrix[i][j])


    def test_compute_distance(self):
        num_of_clients = 6
        num_of_travels = 4
        package_weights = [1, 1, 2, 1, 1, 3]
        distance_matrix = np.ones([10, 10])
        problem_instance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels,
                                                                package_weights, distance_matrix, 1)

        node_1 = problem_instance.get_single_travel_node(0)
        node_2 = problem_instance.get_single_client_node(0)
        self.assertEqual(problem_instance.compute_distance(node_1, node_2), distance_matrix[num_of_clients][0])


if __name__ == '__main__':
    unittest.main()
