from .node import Node


class TravelNode(Node):
    def __init__(self, index: int, x_coordinate, y_coordinate, is_warehouse: bool):
        super().__init__(index, x_coordinate, y_coordinate)
        self.is_warehouse = is_warehouse

    def get_is_warehouse(self):
        return self.is_warehouse

    def __str__(self):
        return "T" + str(self.index) + ("-warehouse" if self.get_is_warehouse() else "")
