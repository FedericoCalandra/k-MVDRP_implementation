import math
from matplotlib import pyplot as plt
from bin.distance_matrix.distance_matrix import DistanceMatrix
from bin.distance_matrix.distance_matrix_generator import DistanceMatrixGenerator
from random import random
from random import seed


NUMBER_OF_DIGITS = 2


def _compute_euclidian_distance(point1, point2):
    return round(math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2)), NUMBER_OF_DIGITS)


class UniformDistanceMatrixGenerator(DistanceMatrixGenerator):

    def __init__(self, random_seed: int):
        self._number_of_travel_nodes = 0
        self._number_of_client_nodes = 0
        self._space_dimension = 0
        self._travel_points = []
        self._client_points = []
        seed(random_seed)

    def generate(self, number_of_travel_nodes: int, number_of_client_nodes: int, space_dimension: float):
        self._number_of_travel_nodes = number_of_travel_nodes
        self._number_of_client_nodes = number_of_client_nodes
        self._space_dimension = space_dimension

        for i in range(number_of_travel_nodes):
            self._travel_points.append([round(space_dimension * random(), NUMBER_OF_DIGITS),
                                        round(space_dimension * random(), NUMBER_OF_DIGITS)])
        for i in range(number_of_client_nodes):
            self._client_points.append([round(space_dimension * random(), NUMBER_OF_DIGITS),
                                        round(space_dimension * random(), NUMBER_OF_DIGITS)])

        distance_matrix = []
        for client_point in self._client_points:
            row = []
            for i in self._client_points:
                row.append(_compute_euclidian_distance([client_point[0], client_point[1]], [i[0], i[1]]))
            for j in self._travel_points:
                row.append(_compute_euclidian_distance([client_point[0], client_point[1]], [j[0], j[1]]))
            distance_matrix.append(row)
        for travel_point in self._travel_points:
            row = []
            for i in self._client_points:
                row.append(_compute_euclidian_distance([travel_point[0], travel_point[1]], [i[0], i[1]]))
            for j in self._travel_points:
                row.append(_compute_euclidian_distance([travel_point[0], travel_point[1]], [j[0], j[1]]))
            distance_matrix.append(row)

        return DistanceMatrix(distance_matrix)

    def get_clients_coordinates(self):
        return self._client_points.copy()

    def get_travels_coordinates(self):
        return self._travel_points.copy()

    def plot_points(self):
        if self._client_points and self._travel_points:
            plt.rcParams["figure.figsize"] = [9.00, 7.50]
            plt.rcParams["figure.autolayout"] = True
            plt.xlim(0, self._space_dimension)
            plt.ylim(0, self._space_dimension)
            plt.grid()
            for v in self._travel_points:
                plt.plot(v[0], v[1], marker="o", markersize=5, markeredgecolor="blue", markerfacecolor="blue")
            for c in self._client_points:
                plt.plot(c[0], c[1], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
            plt.show()
