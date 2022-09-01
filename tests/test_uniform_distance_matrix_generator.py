import math
import unittest
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator


class UniformDistanceMatrixGeneratorTestSuite(unittest.TestCase):
    def test_generate(self):
        generator = UniformDistanceMatrixGenerator(1)
        distance_matrix = generator.generate(5, 10, 250)
        for i in distance_matrix.get_matrix():
            print(i)
        truck_distance_matrix = distance_matrix.get_truck_distance_matrix(10)
        for i in truck_distance_matrix:
            print(i)
        generator.plot_points()
        self.assertEqual(distance_matrix.compute_matrix_dimension(), math.pow(5 + 10, 2))
