from bin.nodes.travel_node import TravelNode
from bin.operations.movement import Movement
from bin.problem_instantiator import ProblemInstance
from bin.veicles.truck import Truck


class TruckTravel(Movement):
    def __init__(self, problem_instance: ProblemInstance, start_node: TravelNode, end_node: TravelNode, truck: Truck):
        super(TruckTravel, self).__init__(start_node, end_node, truck)
        self.problem_instance = problem_instance

    def compute_travel_time(self):
        return self.compute_movement_time(
            self.problem_instance.compute_distance_for_drone(self.start_node, self.end_node))
