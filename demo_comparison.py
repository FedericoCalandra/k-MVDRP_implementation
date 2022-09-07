from bin.distance_matrix.distance_matrix import DistanceMatrix
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator
from bin.optimal_solver import OptimalSolver
from bin.problem_instantiator import ProblemInstance
from bin.rts_solver import RTSSolver
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck
from bin.util.drawer import draw_solution
from random import random, seed
from statistics import mean
import csv


SUPPRESS_OUTPUT = False

NUMBER_OF_CLIENT_NODES = [3]
NUMBER_OF_TRAVEL_NODES = [4]
SPACE_DIMENSION = 10000
SEEDS = [1]
NUMBERS_OF_AVAILABLE_DRONES = [3]


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


class OctocopterEnergyFunction(EnergyFunction):
    def apply(self, flight_distance, carried_weight, is_hovering: bool):
        if carried_weight <= 2.5:
            return (200.00 + ((217.41 - 200.00) * (carried_weight - 0.00))/2.5) * flight_distance
        if carried_weight <= 5.0:
            return (217.41 + ((236.34 - 217.41) * (carried_weight - 2.5))/2.5) * flight_distance
        if carried_weight <= 7.5:
            return (236.34 + ((256.92 - 236.34) * (carried_weight - 5.0))/2.5) * flight_distance
        if carried_weight <= 10.0:
            return (256.92 + ((279.28 - 256.92) * (carried_weight - 7.5))/2.5) * flight_distance
        if carried_weight <= 12.5:
            return (279.28 + ((303.60 - 279.28) * (carried_weight - 10.0))/2.5) * flight_distance
        if carried_weight <= 15.0:
            return (303.60 + ((330.03 - 303.60) * (carried_weight - 12.5))/2.5) * flight_distance
        if carried_weight <= 17.5:
            return (330.03 + ((358.77 - 330.03) * (carried_weight - 15.0))/2.5) * flight_distance
        if carried_weight <= 20.0:
            return (358.77 + ((390.00 - 358.77) * (carried_weight - 17.5))) * flight_distance

    def apply_if_hovering(self, hovering_time: float):
        return 200.000 * hovering_time


TRUCK_SPEED = 10                                                # m/s
TRUCK = Truck(TRUCK_SPEED)

QUADRICOPTER_ENERGY_FUNCTION = QuadricopterEnergyFunction()
QUADRICOPTER_MAX_WEIGHT = 3.000                                 # kg
QUADRICOPTER_MAX_ENERGY_AVAILABLE = [540000 * 1, 900000 * 1]    # Joule*kg
QUADRICOPTER_SPEED = [10, 15]                                   # m/s

OCTOCOPTER_ENERGY_FUNCTION = OctocopterEnergyFunction()
OCTOCOPTER_MAX_WEIGHT = 20.000                                  # kg
OCTOCOPTER_MAX_ENERGY_AVAILABLE = [540000 * 10, 900000 * 10]    # Joule*kg
OCTOCOPTER_SPEED = [10, 15]                                     # m/s

drones = []
for speed in QUADRICOPTER_SPEED:
    for max_energy in QUADRICOPTER_MAX_ENERGY_AVAILABLE:
        drones.append(Drone(speed, QUADRICOPTER_MAX_WEIGHT, max_energy, QUADRICOPTER_ENERGY_FUNCTION))
for speed in OCTOCOPTER_SPEED:
    for max_energy in OCTOCOPTER_MAX_ENERGY_AVAILABLE:
        drones.append(Drone(speed, OCTOCOPTER_MAX_WEIGHT, max_energy, OCTOCOPTER_ENERGY_FUNCTION))


def generate_random_weight_sequence(length, random_seed):
    sequence = []
    seed(random_seed)
    for i in range(length):
        sequence.append(random() * 2.3)
    return sequence


WEIGHTS_SEED = 100


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


with open('computational_results.csv', mode='w') as results:
    results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    results_writer.writerow(["Drone Speed (m/s)", "Energy Density (J/kg)", "Rotors", "k", "RTS Objective Function (s)",
                             "RTS Time (s)", "RTS #feaslible instances", "OPT Objective Function (s)", "OPT Time (s)",
                             "OPT #feasible instances"])
    for drone in drones:
        for k in NUMBERS_OF_AVAILABLE_DRONES:
            number_of_instances = 0

            rts_total_time_list = []
            rts_computational_time_list = []
            rts_number_of_infeasible_instances = 0

            optimal_total_time_list = []
            optimal_computational_time_list = []
            optimal_number_of_infeasible_instances = 0

            for problem_instance in generate_instances(k, drone):
                number_of_instances += 1

                rts_solver = RTSSolver(problem_instance)
                rts_solution = rts_solver.solve()
                rts_total_time_list.append(rts_solution.total_time)
                rts_computational_time_list.append(rts_solution.computational_time)
                if rts_solution.is_infeasible:
                    rts_number_of_infeasible_instances += 1

                optimal_solver = OptimalSolver(problem_instance)
                optimal_solution = optimal_solver.solve()
                optimal_total_time_list.append(optimal_solution.total_time)
                optimal_computational_time_list.append(optimal_solution.computational_time)
                if optimal_solution.is_infeasible:
                    optimal_number_of_infeasible_instances += 1

                if not SUPPRESS_OUTPUT:
                    draw_solution(problem_instance, rts_solution, SPACE_DIMENSION)
                    draw_solution(problem_instance, optimal_solution, SPACE_DIMENSION)

            results_writer.writerow([drone.speed,
                                     drone.max_energy_available,
                                     4 if drone.max_weight == 3 else 8,
                                     k,
                                     round(mean(rts_total_time_list), 2),
                                     round(mean(rts_computational_time_list), 3),
                                     number_of_instances - rts_number_of_infeasible_instances,
                                     round(mean(optimal_total_time_list), 2),
                                     round(mean(optimal_computational_time_list), 3),
                                     number_of_instances - optimal_number_of_infeasible_instances])

print("\n\nTERMINATED")
