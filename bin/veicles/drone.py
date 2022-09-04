from bin.veicles.energy_function import EnergyFunction
from bin.veicles.generic_veicle import Veicle


class Drone(Veicle):
    def __init__(self, speed: float, max_weight: float, max_energy_available: float,
                 energy_usage_per_meter: EnergyFunction):
        super().__init__(speed)
        self.max_weight = max_weight
        self.max_energy_available = max_energy_available
        self._energy_usage = energy_usage_per_meter

    def get_energy_used(self, flight_distance, carried_weight):
        return self._energy_usage.apply(flight_distance, carried_weight, False)

    def get_hov_energy_used(self, hovering_time):
        return self._energy_usage.apply_if_hovering(hovering_time)

    def __str__(self):
        return "Speed: " + str(self.speed) + "   Max weight: " + str(self.max_weight) + \
               "   Max energy available: " + str(self.max_energy_available)
