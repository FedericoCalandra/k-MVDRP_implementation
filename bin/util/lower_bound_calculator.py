import itertools
from bin.nodes.client_node import ClientNode
from bin.nodes.travel_node import TravelNode
from bin.optimal_solver import OptimalSolver
from bin.optimal_solver import cover
import gurobipy as gb
from bin.problem_instantiator import ProblemInstance


class CETSPLowerBoundCalculator:
    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance

    def compute_lower_bound(self):
        env = gb.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        model = gb.Model(env=env)
        x = []

        warehouse_cover_all_clients = True
        for c in self.problem_instance.client_nodes:
            if not self.cover(self.problem_instance.get_warehouse(), c):
                warehouse_cover_all_clients = False
                break
        if warehouse_cover_all_clients:
            return 0

        for i in range(len(self.problem_instance.travel_nodes)):
            row = []
            for j in range(len(self.problem_instance.travel_nodes)):
                row.append(model.addVar(vtype=gb.GRB.BINARY, name=f"x[{i}][{j}]"))
            x.append(row)

        model.modelSense = gb.GRB.MINIMIZE
        model.setObjective(gb.quicksum(
            gb.quicksum(
                self.tt(i, j) * x[i][j] for j in range(len(x[0]))
            ) for i in range(len(x))
        ))

        for c in self.problem_instance.client_nodes:
            model.addConstr(
                gb.quicksum(
                    gb.quicksum(
                        self.cover(self.problem_instance.travel_nodes[i], c) * x[j][i] for j in range(len(x))
                    ) for i in range(len(x[0]))
                ) >= 1, name="cov_constraint"
            )

        for i in range(len(x)):
            model.addConstr(gb.quicksum(x[j][i] for j in range(len(x))) -
                            gb.quicksum(x[i][k] for k in range(len(x[0]))) == 0, name="flow_constraint")

        model.addConstr(gb.quicksum(x[self.problem_instance.get_warehouse().index][i]
                                    for i in range(1, len(x[0]))) == 1,
                        name="warehouse_constraint")

        for sets in self.compute_sets():
            for set_of_nodes in sets:
                U = []
                for node in set_of_nodes:
                    U.append(node.index)
                model.addConstr(gb.quicksum(
                    gb.quicksum(x[i][j] for j in U)
                    for i in U) <= len(U) - 1, name="subtour_elimination"
                                )

        model.optimize()

        return model.ObjVal if model.Status == gb.GRB.OPTIMAL else 0

    def compute_sets(self):
        computed_set = []
        travel_nodes = self.problem_instance.travel_nodes.copy()
        travel_nodes.remove(self.problem_instance.get_warehouse())
        for n in range(2, len(travel_nodes)):
            computed_set.append(set(itertools.permutations(travel_nodes, n)))
        return computed_set

    def cover(self, v: TravelNode, c: ClientNode) -> bool:
        return self.problem_instance.drone.get_energy_used(
            self.problem_instance.compute_distance_for_drone(v, c), c.weight) + \
               self.problem_instance.drone.get_energy_used(
                   self.problem_instance.compute_distance_for_drone(c, v), 0) <= \
               self.problem_instance.drone.max_energy_available

    def tt(self, i: int, j: int):
        distance = self.problem_instance.compute_distance_for_truck(self.problem_instance.travel_nodes[i],
                                                                    self.problem_instance.travel_nodes[j])
        return distance / self.problem_instance.truck.speed if i != j else pow(10, 100)


class RelaxedLowerBoundCalculator:
    def __init__(self, optimal_solver: OptimalSolver):
        self.opt_solver = optimal_solver

    def compute_lower_bound(self):
        env = gb.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        model = gb.Model(env=env)
        times = []
        x = []
        o = self.opt_solver.all_feasible_operations
        for i in range(len(o)):
            x.append(model.addVar(vtype=gb.GRB.BINARY, name=f"x[{i}]"))
            times.append(o[i].compute_operation_time())

        model.modelSense = gb.GRB.MINIMIZE
        model.setObjective(gb.quicksum(times[i] * x[i] for i in range(len(x))))

        for client in self.opt_solver.problem_instance.client_nodes:
            model.addConstr(gb.quicksum(cover(o[i], client) * x[i] for i in range(len(x))) >= 1,
                            name=f"client_constraint{client.index}")

        model.optimize()

        return model.ObjVal if model.Status == gb.GRB.OPTIMAL else 0
