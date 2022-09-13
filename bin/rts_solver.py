import time

from bin.problem_instantiator import ProblemInstance
from bin.util.graph import Graph
from bin.util.rts_solution import RTSSolution
from bin.util.tsp_solver import TSPSolver
import gurobipy as gb


class RTSSolver:
    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance
        self.start_time = time.time()
        self.tsp_obj_value = 0
        self.visit_order = self.route()
        self.graph = self.transform()

    def solve(self):
        return self.shortest_path()

    def route(self):
        nodes = []
        for c in self.problem_instance.client_nodes:
            nodes.append(c.index)
        nodes.append(len(self.problem_instance.client_nodes))   # per il nodo warehouse
        distance_matrix = self.compute_distance_matrix()
        tsp = TSPSolver(nodes, distance_matrix)
        tsp_solution = tsp.solve()
        self.tsp_obj_value = tsp.get_obj_value()
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
                       len(self.problem_instance.travel_nodes) + 1):
            row = []
            for j in range(len(self.problem_instance.drone_distance_matrix.get_matrix()) -
                           len(self.problem_instance.travel_nodes) + 1):
                row.append(self.problem_instance.drone_distance_matrix.get_matrix()[i][j])
            matrix.append(row)
        return matrix

    def transform(self):
        return Graph(self.problem_instance, self.visit_order)

    def shortest_path(self):
        env = gb.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        model = gb.Model(env=env)
        x = []
        costs = []

        for i in range(len(self.graph.edges)):
            x.append(model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name=f"x[{i}]"))
            costs.append(self.graph.edges[i].cost)

        model.modelSense = gb.GRB.MINIMIZE
        model.setObjective(gb.quicksum(costs[i] * x[i] for i in range(len(costs))))

        model.addConstr(gb.quicksum(x[i] for i in self.graph.get_outgoing_edges_indexes(self.graph.get_start_node())) -
                        gb.quicksum(x[i] for i in self.graph.get_entering_edges_indexes(self.graph.get_start_node()))
                        == 1, name="C0")
        model.addConstr(gb.quicksum(x[i] for i in self.graph.get_outgoing_edges_indexes(self.graph.get_end_node())) -
                        gb.quicksum(x[i] for i in self.graph.get_entering_edges_indexes(self.graph.get_end_node()))
                        == -1, name="C1")

        node_list = self.graph.nodes.copy()
        node_list[self.problem_instance.get_warehouse().index] = self.graph.nodes[
            self.problem_instance.get_warehouse().index].copy()
        node_list[self.problem_instance.get_warehouse().index].remove(self.graph.get_start_node())
        node_list[self.problem_instance.get_warehouse().index].remove(self.graph.get_end_node())
        for row in node_list:
            for node in row:
                model.addConstr(gb.quicksum(x[i] for i in self.graph.get_entering_edges_indexes(node)) -
                                gb.quicksum(x[i] for i in self.graph.get_outgoing_edges_indexes(node))
                                == 0, name=f"C {str(node)}")

        model.optimize()

        is_infeasible = model.Status == gb.GRB.INFEASIBLE
        active_edges = []
        total_time = 0
        if not is_infeasible:
            total_time = model.ObjVal
            for i in range(len(x)):
                if x[i].X > 0.5:
                    active_edges.append(self.graph.edges[i])

        return RTSSolution(is_infeasible, total_time, active_edges, time.time() - self.start_time, self.tsp_obj_value)
