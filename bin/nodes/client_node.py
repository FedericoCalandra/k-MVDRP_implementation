from .node import Node


class ClientNode(Node):
    def __init__(self, index, weight):
        super().__init__(index)
        self.weight = weight

    def get_weight(self):
        return self.weight
