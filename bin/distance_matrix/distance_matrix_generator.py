from abc import abstractmethod, ABC

from bin.distance_matrix.distance_matrix import DistanceMatrix


class DistanceMatrixGenerator(ABC):
    @abstractmethod
    def generate(self, number_of_travel_nodes: float, number_of_client_nodes: float, space_dimension: float)\
            -> DistanceMatrix:
        pass
