import unittest
from bin.distance_matrix.uniform_distance_matrix_generator import UniformDistanceMatrixGenerator


class UniformDistanceMatrixGeneratorTestSuite(unittest.TestCase):
    def test_generate(self):
        generator = UniformDistanceMatrixGenerator(1)
        distance_matrix = generator.generate(50, 100, 25000)
        for i in distance_matrix.get_matrix():
            print(i)
        generator.plot_points()
