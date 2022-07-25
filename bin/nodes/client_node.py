from .node import Node


class ClientNode(Node):
    def __init__(self, index, weight):
        super().__init__(index)
        self.weight = weight

    def get_weight(self):
        return self.weight

    def __str__(self):
        return "client_node_index - " + str(self.index) + "   weight - " + str(self.get_weight())
