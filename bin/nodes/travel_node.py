from .node import Node


class TravelNode(Node):
    def __init__(self, index: int, is_warehouse: bool):
        super().__init__(index)
        self.is_warehouse = is_warehouse

    def get_is_warehouse(self):
        return self.is_warehouse

    def __str__(self):
        return "travel_node_index - " + str(self.index) + ("   is the warehouse" if self.get_is_warehouse() else "")