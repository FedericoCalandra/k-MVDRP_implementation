

class DistanceMatrix:
    def __init__(self, matrix_of_distances):
        self.distance_matrix = matrix_of_distances

    def get_matrix(self):
        return self.distance_matrix

    def compute_matrix_dimension(self):
        return len(self.distance_matrix) * len(self.distance_matrix[0])

    def get_truck_distance_matrix(self, number_of_clients: int):
        matrix = []
        for i in range(number_of_clients, len(self.distance_matrix)):
            row = []
            for j in range(number_of_clients, len(self.distance_matrix[0])):
                row.append(self.distance_matrix[i][j])
            matrix.append(row)
        return matrix
