from bin.distance_matrix.distance_matrix import DistanceMatrix
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator
from bin.problem_instantiator import ProblemInstance
from bin.rts_solver import RTSSolver
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck
from bin.util.drawer import draw_solution
from random import random, seed
from statistics import mean
import csv


SUPPRESS_OUTPUT = True

NUMBER_OF_CLIENT_NODES = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
NUMBER_OF_TRAVEL_NODES = [8]
SPACE_DIMENSION = 10000
SEEDS = [1, 2, 3]
NUMBERS_OF_AVAILABLE_DRONES = [2, 4]


class QuadricopterEnergyFunction(EnergyFunction):
    def apply(self, flight_distance, carried_weight, is_hovering: bool):
        if carried_weight <= 0.375:
            return (31.000 + ((33.110 - 31.000) * (carried_weight - 0.000))/0.375) * flight_distance
        if carried_weight <= 0.750:
            return (33.110 + ((35.364 - 33.110) * (carried_weight - 0.375))/0.375) * flight_distance
        if carried_weight <= 1.125:
            return (35.364 + ((37.712 - 35.364) * (carried_weight - 0.750))/0.375) * flight_distance
        if carried_weight <= 1.500:
            return (37.712 + ((40.342 - 37.712) * (carried_weight - 1.125))/0.375) * flight_distance
        if carried_weight <= 1.875:
            return (40.342 + ((43.088 - 40.342) * (carried_weight - 1.500))/0.375) * flight_distance
        if carried_weight <= 2.250:
            return (43.088 + ((46.021 - 43.088) * (carried_weight - 1.875))/0.375) * flight_distance
        if carried_weight <= 2.625:
            return (46.021 + ((49.154 - 46.021) * (carried_weight - 2.250))/0.375) * flight_distance
        if carried_weight <= 3.000:
            return (49.154 + ((52.500 - 49.154) * (carried_weight - 2.625))) * flight_distance

    def apply_if_hovering(self, hovering_time: float):
        return 31.000 * hovering_time


TRUCK_SPEED = 10                                                # m/s
TRUCK = Truck(TRUCK_SPEED)

QUADRICOPTER_ENERGY_FUNCTION = QuadricopterEnergyFunction()
QUADRICOPTER_MAX_WEIGHT = 3.000                                 # kg
QUADRICOPTER_MAX_ENERGY_AVAILABLE = [540000 * 1]                # Joule*kg
QUADRICOPTER_SPEED = [10]                                       # m/s

drones = []
for speed in QUADRICOPTER_SPEED:
    for max_energy in QUADRICOPTER_MAX_ENERGY_AVAILABLE:
        drones.append(Drone(speed, QUADRICOPTER_MAX_WEIGHT, max_energy, QUADRICOPTER_ENERGY_FUNCTION))


def generate_random_weight_sequence(length, random_seed):
    sequence = []
    seed(random_seed)
    for i in range(length):
        sequence.append(random() * 2.3)
    return sequence


WEIGHTS_SEED = 100


TRUCK_DISTANCE_FACTOR = 1.6


def compute_truck_distance_matrix(dm):
    matrix = []
    for row in dm:
        r = []
        for el in row:
            r.append(el * TRUCK_DISTANCE_FACTOR)
        matrix.append(r)
    return matrix


with open('scalability_computational_results.csv', mode='w') as results:
    results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    results_writer.writerow(["Number of Client nodes", "Number of Travel nodes", "k", "RTS Objective Function (s)",
                             "RTS Time (s)", "RTS infeasible instances"])
    counter = 0
    total_number_of_instances_to_be_computed = \
        len(drones) * len(NUMBERS_OF_AVAILABLE_DRONES) * len(NUMBER_OF_CLIENT_NODES) * len(NUMBER_OF_TRAVEL_NODES) * \
        len(SEEDS)
    number_of_instances = 0
    for drone in drones:
        for k in NUMBERS_OF_AVAILABLE_DRONES:
            for n in NUMBER_OF_CLIENT_NODES:
                for m in NUMBER_OF_TRAVEL_NODES:

                    rts_total_time_list = []
                    rts_computational_time_list = []
                    rts_number_of_infeasible_instances = 0

                    for s in SEEDS:
                        generator = UniformDistanceMatrixGenerator(s)
                        distance_matrix = generator.generate(m, n, SPACE_DIMENSION)
                        problem_instance = ProblemInstance(generator.get_clients_coordinates(),
                                                           generator.get_travels_coordinates(),
                                                           generate_random_weight_sequence(n, WEIGHTS_SEED),
                                                           distance_matrix,
                                                           DistanceMatrix(
                                                               compute_truck_distance_matrix(
                                                                   distance_matrix.get_truck_distance_matrix(n))),
                                                           k,
                                                           drone,
                                                           TRUCK)
                        number_of_instances += 1

                        rts_solver = RTSSolver(problem_instance)
                        rts_solution = rts_solver.solve()
                        rts_total_time_list.append(rts_solution.total_time)
                        rts_computational_time_list.append(rts_solution.computational_time)

                        if rts_solution.is_infeasible:
                            rts_number_of_infeasible_instances += 1

                        counter += 1
                        print(f"PROGRESS: {(100 * counter) / total_number_of_instances_to_be_computed}%\n"
                              f"Computed: {counter}/{total_number_of_instances_to_be_computed} instances\n\n")

                        if not SUPPRESS_OUTPUT:
                            print("\n\nRTS Graph\n", rts_solver.graph)
                            draw_solution(problem_instance, rts_solution, SPACE_DIMENSION)

                    results_writer.writerow([len(problem_instance.client_nodes),
                                             len(problem_instance.travel_nodes),
                                             k,
                                             round(mean(rts_total_time_list), 2),
                                             round(mean(rts_computational_time_list), 3),
                                             rts_number_of_infeasible_instances])

print("\n\nTERMINATED")
