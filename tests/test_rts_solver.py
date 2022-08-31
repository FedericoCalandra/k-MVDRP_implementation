import unittest
from bin import problem_instantiator
from bin.basic_solver import BasicSolver
from bin.rts_solver import RTSSolver
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


class RTSSolverTestSuite(unittest.TestCase):

    def setUp(self):
        class Exp(EnergyFunction):
            def apply(self, flight_time, carried_weight, is_hovering: bool):
                if is_hovering:
                    return 1 * flight_time
                return 1 * flight_time * carried_weight

        self.package_weights = [1, 1, 2, 1, 1, 3]
        self.drone_distance_matrix = [[0, 7, 10, 5, 5.4, 12],
                                      [7, 0, 7, 5, 3, 8.6],
                                      [10, 7, 0, 11.1, 5.4, 2],
                                      [5, 5, 11.1, 0, 5.8, 13],
                                      [5.4, 3, 5.4, 5.8, 0, 7.3],
                                      [12, 8.6, 2, 13, 7.3, 0]]
        self.truck_distance_matrix = [[0, 5.8, 13],
                                      [5.8, 0, 7.3],
                                      [13, 7.3, 0]]

        self.num_of_clients = len(self.drone_distance_matrix) - len(self.truck_distance_matrix)
        self.num_of_travels = len(self.truck_distance_matrix)
        self.drone_time_matrix = self.drone_distance_matrix
        self.truck_time_matrix = self.truck_distance_matrix
        self.drone = Drone(10.0, 5.0, 0.1, Exp())
        self.truck = Truck(10)
        self.problem_instance = problem_instantiator.ProblemInstance(self.num_of_clients, self.num_of_travels,
                                                                     self.package_weights, self.drone_time_matrix,
                                                                     self.truck_time_matrix, 1, self.drone, self.truck)
        self.problem_instance.set_warehouse(0)
        self.rts_solver = RTSSolver(self.problem_instance)

    def test_route(self):
        print("\nPROBLEM INSTANCE" + "\nnumber of clients: " + str(self.num_of_clients) + "\nnumber of travel node: " +
              str(self.num_of_travels) + "\ndrone: " + str(self.drone) + "\ntruck: " + str(self.truck))
        print("---visit order---")
        for node in self.rts_solver.visit_order:
            print(node)
        print("-----------------")

    def test_transform(self):
        print("\nGRAPH")
        print(self.rts_solver.graph)

    def test_shortest_path(self):
        print("\n")
        solution = self.rts_solver.shortest_path()
        print("is feasible = " + str(not solution.is_infeasible))
        print("-----ACTIVE EDGES-----")
        if not solution.is_infeasible:
            for edge in solution.active_edges:
                print(edge)
        print("----------------------")
        print("Total time: " + str(solution.total_time) + "\nComputational time: " + str(solution.computational_time))
