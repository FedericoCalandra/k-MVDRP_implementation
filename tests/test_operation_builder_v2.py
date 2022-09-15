from random import random, seed
from bin.distance_matrix.distance_matrix import DistanceMatrix
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator
from bin.operations.flight import Flight
from bin.problem_instantiator import ProblemInstance
from bin.rts_solver_modified import RTSSolverV2
from bin.util.operation_builder_modified import OperationBuilderV2
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck

NUMBER_OF_CLIENT_NODES = [5]
NUMBER_OF_TRAVEL_NODES = [3]
SPACE_DIMENSION = 10000
SEEDS = [2]
NUMBERS_OF_AVAILABLE_DRONES = [2]


class QuadricopterEnergyFunction(EnergyFunction):
    def apply(self, flight_time, carried_weight, is_hovering: bool):
        if carried_weight <= 0.375:
            return 31.000 + ((33.110 - 31.000) * (carried_weight - 0.000))/0.375
        if carried_weight <= 0.750:
            return 33.110 + ((35.364 - 33.110) * (carried_weight - 0.375))/0.375
        if carried_weight <= 1.125:
            return 35.364 + ((37.712 - 35.364) * (carried_weight - 0.750))/0.375
        if carried_weight <= 1.500:
            return 37.712 + ((40.342 - 37.712) * (carried_weight - 1.125))/0.375
        if carried_weight <= 1.875:
            return 40.342 + ((43.088 - 40.342) * (carried_weight - 1.500))/0.375
        if carried_weight <= 2.250:
            return 43.088 + ((46.021 - 43.088) * (carried_weight - 1.875))/0.375
        if carried_weight <= 2.625:
            return 46.021 + ((49.154 - 46.021) * (carried_weight - 2.250))/0.375
        if carried_weight <= 3.000:
            return 49.154 + ((52.500 - 49.154) * (carried_weight - 2.625))

    def apply_if_hovering(self, hovering_time: float):
        return 31.000 * hovering_time


class OctocopterEnergyFunction(EnergyFunction):
    def apply(self, flight_time, carried_weight, is_hovering: bool):
        if carried_weight <= 2.5:
            return 200.00 + ((217.41 - 200.00) * (carried_weight - 0.00))/2.5
        if carried_weight <= 5.0:
            return 217.41 + ((236.34 - 217.41) * (carried_weight - 2.5))/2.5
        if carried_weight <= 7.5:
            return 236.34 + ((256.92 - 236.34) * (carried_weight - 5.0))/2.5
        if carried_weight <= 10.0:
            return 256.92 + ((279.28 - 256.92) * (carried_weight - 7.5))/2.5
        if carried_weight <= 12.5:
            return 279.28 + ((303.60 - 279.28) * (carried_weight - 10.0))/2.5
        if carried_weight <= 15.0:
            return 303.60 + ((330.03 - 303.60) * (carried_weight - 12.5))/2.5
        if carried_weight <= 17.5:
            return 330.03 + ((358.77 - 330.03) * (carried_weight - 15.0))/2.5
        if carried_weight <= 20.0:
            return 358.77 + ((390.00 - 358.77) * (carried_weight - 17.5))

    def apply_if_hovering(self, hovering_time: float):
        return 200.000 * hovering_time


TRUCK_SPEED = 15                                                # m/s
TRUCK = Truck(TRUCK_SPEED)

QUADRICOPTER_ENERGY_FUNCTION = QuadricopterEnergyFunction()
QUADRICOPTER_MAX_WEIGHT = 3.000                                 # kg
QUADRICOPTER_MAX_ENERGY_AVAILABLE = [540.00 * 1]   # Joule*kg
QUADRICOPTER_SPEED = [10]                                       # m/s

OCTOCOPTER_ENERGY_FUNCTION = OctocopterEnergyFunction()
OCTOCOPTER_MAX_WEIGHT = 20.000                                  # kg
OCTOCOPTER_MAX_ENERGY_AVAILABLE = [540.00 * 10]   # Joule*kg
OCTOCOPTER_SPEED = [10]                                         # m/s

drones = []
for max_energy in QUADRICOPTER_MAX_ENERGY_AVAILABLE:
    for speed in QUADRICOPTER_SPEED:
        drones.append(Drone(speed, QUADRICOPTER_MAX_WEIGHT, max_energy, QUADRICOPTER_ENERGY_FUNCTION))
for max_energy in OCTOCOPTER_MAX_ENERGY_AVAILABLE:
    for speed in OCTOCOPTER_SPEED:
        drones.append(Drone(speed, OCTOCOPTER_MAX_WEIGHT, max_energy, OCTOCOPTER_ENERGY_FUNCTION))


def generate_random_weight_sequence(length, random_seed):
    sequence = []
    seed(random_seed)
    for i in range(length):
        sequence.append(random() * 2.3)
    return sequence


WEIGHTS_SEED = 100


problem_instances = []
for n in NUMBER_OF_CLIENT_NODES:
    for m in NUMBER_OF_TRAVEL_NODES:
        for k in NUMBERS_OF_AVAILABLE_DRONES:
            for s in SEEDS:
                for drone in drones:
                    generator = UniformDistanceMatrixGenerator(s)
                    distance_matrix = generator.generate(m, n, SPACE_DIMENSION)
                    problem_instances.append(ProblemInstance(generator.get_clients_coordinates(),
                                                             generator.get_travels_coordinates(),
                                                             generate_random_weight_sequence(n, WEIGHTS_SEED),
                                                             distance_matrix,
                                                             DistanceMatrix(distance_matrix.
                                                                            get_truck_distance_matrix(n)),
                                                             k,
                                                             drone,
                                                             TRUCK))

s = RTSSolverV2(problem_instances[1])
ob = OperationBuilderV2(problem_instances[1], problem_instances[1].travel_nodes[0], problem_instances[1].travel_nodes[0],
                        6, 0, s.visit_order)
operation = ob.build_operation()
f1 = Flight(problem_instances[1].travel_nodes[0], problem_instances[1].travel_nodes[0], s.visit_order[0:2],
            problem_instances[1].drone)
f2 = Flight(problem_instances[1].travel_nodes[0], problem_instances[1].travel_nodes[0], s.visit_order[3:5],
            problem_instances[1].drone)
print("time(f1) = " + str(f1.compute_flight_time(problem_instances[1])))
print("time(f2) = " + str(f2.compute_flight_time(problem_instances[1])))
print(str(operation.flights))
