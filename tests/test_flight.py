import unittest
import numpy as np
from bin import problem_instantiator
from bin.operations.flight import Flight
from bin.veicles.drone import Drone
from bin.veicles.energy_function import EnergyFunction
from bin.veicles.truck import Truck


class FlightTestSuite(unittest.TestCase):

    def test_flight(self):
        num_of_clients_node = 2
        num_of_travels_node = 2
        package_weights = [2, 2]
        length = num_of_clients_node + num_of_travels_node
        drone = Drone(3.0, 10, 1, EnergyFunction())
        truck = Truck(0.4)
        drone_distance_matrix = np.ones([length, length])*2
        truck_distance_matrix = np.ones([length, length])

        problem_instance = problem_instantiator.ProblemInstance(num_of_clients_node, num_of_travels_node,
                                                                package_weights, drone_distance_matrix,
                                                                truck_distance_matrix, 3, drone, truck)

        flight = Flight(problem_instance.get_single_travel_node(0), problem_instance.get_single_travel_node(1),
                        problem_instance.get_list_of_client_nodes(), drone)

        print("Takeoff node: ", flight.takeoff_node, "\nLanding node: ", flight.landing_node)
        for c in flight.visited_clients:
            print("Visited client: " + str(c))
        print("Drone specs: ", flight.drone)
        print("Flight time: ", flight.compute_flight_time(problem_instance))
        energy_computed = flight.compute_energy_used_for_flight(problem_instance)
        print("Energy used = " + str(energy_computed))

        self.assertEqual(flight.takeoff_node.index, 0)
        self.assertEqual(flight.landing_node.index, 1)
        self.assertEqual(flight.drone, drone)
        #self.assertEqual(energy_computed, 2)
