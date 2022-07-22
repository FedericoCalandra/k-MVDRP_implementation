import unittest
import numpy as np
from bin import problem_instantiator


class ProblemInstanceTestSuite(unittest.TestCase):

    def test_instanceProblem_getters(self):
        num_of_clients = 6
        num_of_travels = 4
        package_weights = [1, 1, 2, 1, 1, 3]
        distance_matrix = np.ones([10, 10])
        problem_instance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels,
                                                                package_weights, distance_matrix)

        for i in range(len(problem_instance.client_nodes)):
            self.assertEqual(problem_instance.client_nodes[i].index, i)
            self.assertEqual(problem_instance.client_nodes[i].weight, package_weights[i])

        for i in range(len(problem_instance.travel_nodes)):
            self.assertEqual(problem_instance.travel_nodes[i].index, i)
            self.assertEqual(problem_instance.travel_nodes[i].is_warehouse, i == 0)

        for i in range(len(problem_instance.distance_matrix)):
            for j in range(len(problem_instance.distance_matrix[i])):
                self.assertEqual(problem_instance.get_distance(i, j), distance_matrix[i][j])


if __name__ == '__main__':
    unittest.main()
