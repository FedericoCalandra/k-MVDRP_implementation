import unittest
from bin import problem_instantiator


class ProblemInstanceTestSuite(unittest.TestCase):

    def test_instanceProblem_getters(self):
        num_of_clients = 6
        num_of_travels = 4
        distanceMatrix = [[0, 1, 1], [1, 0, 1], [0, 0, 1]]
        problemInstance = problem_instantiator.ProblemInstance(num_of_clients, num_of_travels, distanceMatrix)

        self.assertEqual(problemInstance.get_client_nodes(), [_ for _ in range(num_of_clients)])
        self.assertEqual(problemInstance.get_travel_nodes(), [_ for _ in range(num_of_travels)])
        for index in range(num_of_clients):
            self.assertEqual(problemInstance.get_single_client_node(index), [index])
        self.assertEqual(problemInstance.get_distance_matrix(), distanceMatrix)
        for i in range(len(distanceMatrix)):
            for j in range(len(distanceMatrix[i])):
                self.assertEqual(problemInstance.get_distance(i, j), distanceMatrix[i][j])


if __name__ == '__main__':
    unittest.main()
