from bin.veicles.energy_function import EnergyFunction
from bin.veicles.generic_veicle import Veicle


class Drone(Veicle):
    def __init__(self, speed: float, max_weight: float, energy_usage_per_time_unit: EnergyFunction):
        super().__init__(speed)
        self.max_weight = max_weight
        self.energy_usage_per_time_unit = energy_usage_per_time_unit
