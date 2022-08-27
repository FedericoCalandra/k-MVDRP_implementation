from itertools import combinations
import gurobipy as gp
from gurobipy import GRB


def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                if vals[i, j] > 0.5)
        clients = [i for i in range(len(model._vars))]
        tour = subtour(selected, clients)
        if len(tour) < len(clients):
            model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                         <= len(tour) - 1)


def subtour(edges, clients):
    unvisited = clients[:]
    cycle = clients[:]
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
    def __init__(self, clients, distance_matrix):
        self.clients = clients
        self.distance_matrix = distance_matrix
        self.dist = {(c1, c2): self.distance(c1, c2) for c1, c2 in combinations(self.clients, 2)}

    def distance(self, client1, client2):
        return self.distance_matrix[client1][client2]

    def solve(self):
        m = gp.Model()
        vars = m.addVars(self.dist.keys(), obj=self.dist, vtype=GRB.BINARY, name='x')
        for i, j in vars.keys():
            vars[j, i] = vars[i, j]
        cons = m.addConstrs(vars.sum(c, '*') == 2 for c in self.clients)
        m._vars = vars
        m.Params.lazyConstraints = 1
        m.optimize(subtourelim)
        vals = m.getAttr('x', vars)
        selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
        tour = subtour(selected, self.clients)
        assert len(tour) == len(self.clients)
