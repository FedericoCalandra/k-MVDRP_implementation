from itertools import combinations
import gurobipy as gp
from gurobipy import GRB


def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                if vals[i, j] > 0.5)
        nodes = [i for i in range(len(model.getConstrs()))]
        tour = subtour(selected, nodes)
        if len(tour) < len(nodes):
            model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                         <= len(tour) - 1)


def subtour(edges, nodes):
    unvisited = nodes[:]
    cycle = nodes[:]
    while unvisited:
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(thiscycle) <= len(cycle):
            cycle = thiscycle
    return cycle


class TSPSolver:
    def __init__(self, nodes, distance_matrix):
        self.clients = nodes
        self.distance_matrix = distance_matrix
        self.dist = {(c1, c2): self.distance(c1, c2) for c1, c2 in combinations(self.clients, 2)}
        self.problem_variables = None
        self.model = None

    def distance(self, client1, client2):
        return self.distance_matrix[client1][client2]

    def solve(self):
        env = gp.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        m = gp.Model(env=env)
        self.problem_variables = m.addVars(self.dist.keys(), obj=self.dist, vtype=GRB.BINARY, name='x')
        for i, j in self.problem_variables.keys():
            self.problem_variables[j, i] = self.problem_variables[i, j]
        cons = m.addConstrs(self.problem_variables.sum(c, '*') == 2 for c in self.clients)
        m._vars = self.problem_variables
        m.Params.lazyConstraints = 1
        m.optimize(subtourelim)
        vals = m.getAttr('x', self.problem_variables)
        selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
        tour = subtour(selected, self.clients)
        assert len(tour) == len(self.clients)
        self.model = m
        return self.get_solution()

    def get_solution(self):
        solution = []
        for i in range(len(self.clients)):
            row = []
            for j in range(len(self.clients)):
                if i != j and self.problem_variables[(i, j)].X > 0.5:
                    row.append(1)
                else:
                    row.append(0)
            solution.append(row)
        return solution

    def get_obj_value(self):
        return self.model.ObjVal
