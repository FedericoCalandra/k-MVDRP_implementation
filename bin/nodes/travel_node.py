from .node import Node


class TravelNode(Node):
    def __init__(self, index: int, is_warehouse: bool):
        super().__init__(index)
        self.is_warehouse = is_warehouse

    def get_is_warehouse(self):
        return self.is_warehouse
