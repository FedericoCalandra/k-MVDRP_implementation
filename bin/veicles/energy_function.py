# still to implement!!!

class EnergyFunction:
    def __init__(self):
        self.energy_function = 1                    #da implementare!!!

    def apply(self, flight_time, carried_weight, is_hovering: bool):
        if is_hovering:
            return self.energy_function * flight_time
        return self.energy_function * flight_time * carried_weight
    