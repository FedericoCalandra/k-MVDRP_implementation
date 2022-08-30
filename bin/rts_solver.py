from bin.problem_instantiator import ProblemInstance
from bin.util.graph import Graph
from bin.util.tsp_solver import TSPSolver


class RTSSolver:
    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance
        self.visit_order = self.route()
        self.graph = self.transform()

    def route(self):
        nodes = []
        for c in self.problem_instance.client_nodes:
            nodes.append(c.index)
        nodes.append(len(self.problem_instance.client_nodes))   # per il nodo warehouse
        distance_matrix = self.compute_distance_matrix()
        tsp = TSPSolver(nodes, distance_matrix)
        tsp_solution = tsp.solve()
        return self.compute_visit_order(tsp_solution)

    def compute_visit_order(self, solution):
        visit_order = [len(solution) - 1]
        for position in range(len(solution)):
            current_node = visit_order[position]
            for i in range(len(solution[current_node])):
                if solution[current_node][i] == 1 and i not in visit_order:
                    visit_order.append(i)
                    position += 1
                    break
        nodes_visit_order = []
        for index in visit_order:
            if index < len(solution) - 1:
                nodes_visit_order.append(self.problem_instance.client_nodes[index])
        return nodes_visit_order

    def compute_distance_matrix(self):
        matrix = []
        for i in range(len(self.problem_instance.drone_distance_matrix.get_matrix()) -
                       len(self.problem_instance.client_nodes) + 1):
            row = []
            for j in range(len(self.problem_instance.drone_distance_matrix.get_matrix()) -
                           len(self.problem_instance.client_nodes) + 1):
                row.append(self.problem_instance.drone_distance_matrix.get_matrix()[i][j])
            matrix.append(row)
        return matrix

    def transform(self):
        return Graph(self.problem_instance, self.visit_order)

    def shortest_path(self):
        pass