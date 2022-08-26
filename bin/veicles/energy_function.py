from abc import abstractmethod, ABC


class EnergyFunction(ABC):
    @abstractmethod
    def apply(self, flight_time, carried_weight, is_hovering: bool):
        pass
    