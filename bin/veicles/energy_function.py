from abc import abstractmethod, ABC


class EnergyFunction(ABC):
    @abstractmethod
    def apply(self, flight_distance, carried_weight, is_hovering: bool):
        if is_hovering:
            return self.apply_if_hovering()
        pass

    @abstractmethod
    def apply_if_hovering(self, hovering_time: float):
        pass
    