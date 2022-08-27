import unittest
from bin.nodes.client_node import ClientNode
from bin.util.tsp_solver import TSPSolver


class TSPSolverTestSuite(unittest.TestCase):

    def test_solver(self):
        clients = [i for i in range(4)]
        distance_matrix = [[100, 1, 6, 1],
                           [1, 100, 20, 7],
                           [6, 20, 100, 5],
                           [1, 7, 5, 100]]
        tsp = TSPSolver(clients, distance_matrix)
        tsp.solve()
