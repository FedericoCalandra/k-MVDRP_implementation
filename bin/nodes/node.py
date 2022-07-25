class Node:
    def __init__(self, index: int):
        self.index = index

    def get_index(self):
        return self.index

    def __str__(self):
        return "generic_node_index - " + str(self.index)
