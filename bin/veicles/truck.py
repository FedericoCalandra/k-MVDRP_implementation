from bin.veicles.generic_veicle import Veicle


class Truck(Veicle):
    def __init__(self, speed: float):
        super().__init__(speed)

    def __str__(self):
        return "Truck, speed: " + str(self.speed)