from bin.nodes.travel_node import TravelNode
from bin.operations.movement import Movement
from bin.veicles.truck import Truck


class Operation:
    def __init__(self, start_node: TravelNode, end_node: TravelNode, flights, truck: Truck):
        self.flights = flights
        self.truck_movement = Movement(start_node, end_node, truck)
