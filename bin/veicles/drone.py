from bin.veicles.energy_function import EnergyFunction
from bin.veicles.generic_veicle import Veicle


class Drone(Veicle):
    def __init__(self, speed: float, max_weight: float, max_energy_available: float,
                 energy_usage_per_time_unit: EnergyFunction):
        super().__init__(speed)
        self.max_weight = max_weight
        self.max_energy_available = max_energy_available
        self._energy_usage_per_time_unit = energy_usage_per_time_unit

    def get_energy_used(self, flight_time, carried_weight):
        return self._energy_usage_per_time_unit.apply(flight_time, carried_weight, False)

    def get_hov_energy_used(self, hovering_time):
        return self._energy_usage_per_time_unit.apply(hovering_time, 0, True)

    def __str__(self):
        return "Speed: " + str(self.speed) + "   Max weight: " + str(self.max_weight) + \
               "   Max energy available: " + str(self.max_energy_available)
