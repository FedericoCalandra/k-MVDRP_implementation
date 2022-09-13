from bin.distance_matrix.distance_matrix import DistanceMatrix
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator
from bin.problem_instantiator import ProblemInstance
from random import random, seed
import unittest
from bin.optimal_solver import OptimalSolver
from bin.util.drawer import draw_solution
from bin.util.lower_bound_calculator import RelaxedLowerBoundCalculator, CETSPLowerBoundCalculator
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


SUPPRESS_OUTPUT = True
NUMBER_OF_CLIENT_NODES = [5]
NUMBER_OF_TRAVEL_NODES = [5]
SPACE_DIMENSION = 10000
SEEDS = [1]
TRUCK_SPEED = 10  # m/s
TRUCK = Truck(TRUCK_SPEED)


class QuadricopterEnergyFunction(EnergyFunction):
    def apply(self, flight_distance, carried_weight, is_hovering: bool):
        if carried_weight <= 0.375:
            return (31.000 + ((33.110 - 31.000) * (carried_weight - 0.000)) / 0.375) * flight_distance
        if carried_weight <= 0.750:
            return (33.110 + ((35.364 - 33.110) * (carried_weight - 0.375)) / 0.375) * flight_distance
        if carried_weight <= 1.125:
            return (35.364 + ((37.712 - 35.364) * (carried_weight - 0.750)) / 0.375) * flight_distance
        if carried_weight <= 1.500:
            return (37.712 + ((40.342 - 37.712) * (carried_weight - 1.125)) / 0.375) * flight_distance
        if carried_weight <= 1.875:
            return (40.342 + ((43.088 - 40.342) * (carried_weight - 1.500)) / 0.375) * flight_distance
        if carried_weight <= 2.250:
            return (43.088 + ((46.021 - 43.088) * (carried_weight - 1.875)) / 0.375) * flight_distance
        if carried_weight <= 2.625:
            return (46.021 + ((49.154 - 46.021) * (carried_weight - 2.250)) / 0.375) * flight_distance
        if carried_weight <= 3.000:
            return (49.154 + ((52.500 - 49.154) * (carried_weight - 2.625))) * flight_distance

    def apply_if_hovering(self, hovering_time: float):
        return 31.000 * hovering_time


QUADRICOPTER_ENERGY_FUNCTION = QuadricopterEnergyFunction()
QUADRICOPTER_MAX_WEIGHT = 3.000  # kg
QUADRICOPTER_MAX_ENERGY_AVAILABLE = [540000 * 1]  # Joule*kg
QUADRICOPTER_SPEED = [10]  # m/s

drone = Drone(QUADRICOPTER_SPEED[0], QUADRICOPTER_MAX_WEIGHT, QUADRICOPTER_MAX_ENERGY_AVAILABLE[0],
              QUADRICOPTER_ENERGY_FUNCTION)

WEIGHTS_SEED = 100


def generate_random_weight_sequence(length, random_seed):
    sequence = []
    seed(random_seed)
    for i in range(length):
        sequence.append(random() * 2.3)
    return sequence


def generate_instances(num_of_drones, drone_type):
    problem_instances = []
    for n in NUMBER_OF_CLIENT_NODES:
        for m in NUMBER_OF_TRAVEL_NODES:
            for s in SEEDS:
                generator = UniformDistanceMatrixGenerator(s)
                distance_matrix = generator.generate(m, n, SPACE_DIMENSION)
                problem_instances.append(ProblemInstance(generator.get_clients_coordinates(),
                                                         generator.get_travels_coordinates(),
                                                         generate_random_weight_sequence(n, WEIGHTS_SEED),
                                                         distance_matrix,
                                                         DistanceMatrix(distance_matrix.
                                                                        get_truck_distance_matrix(n)),
                                                         num_of_drones,
                                                         drone_type,
                                                         TRUCK))
    return problem_instances


class BasicSolverTestSuite(unittest.TestCase):

    def setUp(self):
        self.problem_instance = generate_instances(2, drone)[0]
        self.optimal_solver = OptimalSolver(self.problem_instance)

    # truck movement test
    def test_truck_movement(self):
        truck_movements = self.optimal_solver.compute_all_feasible_truck_movements()
        print("\nTRUCK MOVEMENTS COMPUTED")
        for movement in truck_movements:
            print(movement)

    # all ops test
    def test_compute_all_feasible_operations(self):
        all_operations = self.optimal_solver.all_feasible_operations
        # print("ALL FEASIBLE OPERATIONS COMPUTED")
        # for operation in all_operations:
        #     print(operation)
        print("Total number of feasible operations: " + str(len(all_operations)))

    def test_solve(self):
        print("\n\nSOLVE\n\n")
        solution = self.optimal_solver.solve()
        draw_solution(self.problem_instance, solution, SPACE_DIMENSION)

    def test_lower_bound_1_calculator(self):
        lb_calc = RelaxedLowerBoundCalculator(self.optimal_solver)
        print("Lower Bound = " + str(lb_calc.compute_lower_bound_1()))

    def test_lower_bound_2_calculator(self):
        lb_calc = CETSPLowerBoundCalculator(self.problem_instance)
        print("Lower Bound = " + str(lb_calc.compute_lower_bound()))



if __name__ == '__main__':
    unittest.main()
