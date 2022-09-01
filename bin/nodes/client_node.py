from .node import Node


class ClientNode(Node):
    def __init__(self, index: int, x_coordinate, y_coordinate, weight):
        super().__init__(index, x_coordinate, y_coordinate)
        self.weight = weight

    def get_weight(self):
        return self.weight

    def __str__(self):
        return "C" + str(self.index)
