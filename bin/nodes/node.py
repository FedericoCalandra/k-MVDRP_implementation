class Node:
    def __init__(self, index: int, x_coordinate, y_coordinate):
        self.index = index
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def get_index(self):
        return self.index

    def __str__(self):
        return "generic_node_index - " + str(self.index)
