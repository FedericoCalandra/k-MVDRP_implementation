import unittest
from bin import problem_instantiator
from bin.basic_solver import BasicSolver
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


class BasicSolverTestSuite(unittest.TestCase):

    def setUp(self):
        self.package_weights = [1, 1, 2, 1, 1, 3]
        self.drone_distance_matrix_1 = [[0, 7, 10, 9.4, 5.4, 5, 5.4, 12, 8.5, 5.4, 3.6],
                                        [7, 0, 7, 10.4, 10.4, 5, 3, 8.6, 8.5, 7, 10.6],
                                        [10, 7, 0, 5.4, 9.4, 11.1, 5.4, 2, 3.6, 5.4, 12.4],
                                        [9.4, 10.4, 5.4, 0, 6, 12.8, 7.6, 6.4, 2, 4.2, 10.2],
                                        [5.4, 10.4, 9.4, 6, 0, 10.2, 7.6, 11.2, 6.3, 4.2, 4.5],
                                        [5, 5, 11.1, 12.8, 10.2, 0, 5.8, 13, 11.3, 8.6, 8.2],
                                        [5.4, 3, 5.4, 7.6, 7.6, 5.8, 0, 7.3, 5.8, 4, 8.6],
                                        [12, 8.6, 2, 6.4, 11.2, 13, 7.3, 0, 5, 7.3, 14.3],
                                        [8.5, 8.5, 3.6, 2, 6.3, 11.3, 5.8, 5, 0, 3.2, 10],
                                        [5.4, 7, 5.4, 4.2, 4.2, 8.6, 4, 7.3, 3.2, 0, 7.1],
                                        [3.6, 10.6, 12.4, 10.2, 4.5, 8.2, 8.6, 14.3, 10, 7.1, 0]]
        self.truck_distance_matrix_1 = [[0, 7, 10, 9.4, 5.4],
                                        [7, 0, 7, 10.4, 10.4],
                                        [10, 7, 0, 5.4, 9.4],
                                        [9.4, 10.4, 5.4, 0, 6],
                                        [5.4, 10.4, 9.4, 6, 0]]
        self.drone_distance_matrix_2 = [[0, 7, 10, 5, 5.4, 12],
                                        [7, 0, 7, 5, 3, 8.6],
                                        [10, 7, 0, 11.1, 5.4, 2],
                                        [5, 5, 11.1, 0, 5.8, 13],
                                        [5.4, 3, 5.4, 5.8, 0, 7.3],
                                        [12, 8.6, 2, 13, 7.3, 0]]
        self.truck_distance_matrix_2 = [[0, 7, 10],
                                        [7, 0, 7],
                                        [10, 7, 0]]

        self.num_of_clients = len(self.drone_distance_matrix_2) - len(self.truck_distance_matrix_2)
        self.num_of_travels = len(self.truck_distance_matrix_2)
        self.drone_time_matrix = self.drone_distance_matrix_2
        self.truck_time_matrix = self.truck_distance_matrix_2
        self.drone = Drone(10.0, 5.0, 2, EnergyFunction())
        self.truck = Truck(10)
        self.problem_instance = problem_instantiator.ProblemInstance(self.num_of_clients, self.num_of_travels,
                                                                     self.package_weights, self.drone_time_matrix,
                                                                     self.truck_time_matrix, 2, self.drone, self.truck)
        self.basic_solver = BasicSolver(self.problem_instance)

    # truck movement test
    def test_truck_movement(self):
        truck_movements = self.basic_solver.compute_all_feasible_truck_movements()
        print("\nTRUCK MOVEMENTS COMUTED")
        for movement in truck_movements:
            print(movement)
        self.assertEqual(len(truck_movements), pow(len(self.truck_distance_matrix_2), 2))

    # all ops test
    def test_compute_all_feasible_operations(self):
        all_operations = self.basic_solver.compute_all_feasible_operations()
        print("ALL FEASIBLE OPERATIONS COMPUTED")
        for operation in all_operations:
            print(operation)


if __name__ == '__main__':
    unittest.main()
