import itertools
import gurobipy as gb
from bin.nodes.client_node import ClientNode
from bin.nodes.node import Node
from bin.operations.flight import Flight
from bin.operations.operation import Operation
from bin.problem_instantiator import ProblemInstance


class OperationBuilderV2:
    def __init__(self, problem_instance: ProblemInstance, start_node: Node, end_node: Node,
                 number_of_clients_to_be_served: int, number_of_served_clients: int, visit_order: list[ClientNode]):
        self.problem_instance = problem_instance
        self.start_node = start_node
        self.end_node = end_node
        self.number_of_clients_to_be_served = number_of_clients_to_be_served
        self.number_of_served_clients = number_of_served_clients
        self.visit_order = visit_order.copy()
        self.clients_to_be_visited = self.visit_order[self.number_of_served_clients:self.number_of_clients_to_be_served]

    def build_operation(self):
        # noinspection PyTypeChecker
        operation = Operation(self.problem_instance, self.start_node, self.end_node,
                              self.compute_flights_in_operation(), self.problem_instance.truck)
        return operation if operation.is_feasible() else None

    def compute_all_flights(self):
        flights = []
        for i in range(1, len(self.clients_to_be_visited) - (self.problem_instance.number_of_available_drones - 2)):
            combinations = itertools.permutations(self.clients_to_be_visited, i)
            for j in combinations:
                flights.append(Flight(self.start_node, self.end_node, list(j), self.problem_instance.drone))
        return flights

    @staticmethod
    def cover(flight: Flight, client: ClientNode) -> bool:
        for c in flight.visited_clients:
            if c == client:
                return True
        return False

    def compute_flights_in_operation(self):
        flights = []
        if len(self.clients_to_be_visited) > self.problem_instance.number_of_available_drones:
            x = []
            z = []
            all_flights = self.compute_all_flights()
            env = gb.Env(empty=True)
            env.setParam("OutputFlag", 0)
            env.start()
            model = gb.Model(env=env)

            for i in range(len(all_flights)):
                x.append(model.addVar(vtype=gb.GRB.BINARY, name=f"x[{i}]"))

            for i in range(len(all_flights)):
                z.append(model.addVar(vtype=gb.GRB.CONTINUOUS, name=f"z[{i}]"))

            y = model.addVar(vtype=gb.GRB.CONTINUOUS, name="y")

            model.modelSense = gb.GRB.MINIMIZE
            model.setObjective(y)

            for i in range(len(all_flights)):
                model.addConstr(z[i] == all_flights[i].compute_flight_time(self.problem_instance) * x[i])

            model.addConstr(y == gb.max_(z))

            for c in self.clients_to_be_visited:
                model.addConstr(gb.quicksum(self.cover(all_flights[i], c) * x[i]
                                            for i in range(len(all_flights))) == 1,
                                name=f"constr_c[{c.index}]")

            for i in range(len(all_flights)):
                model.addConstr(gb.quicksum(self.cover(all_flights[i], c) * c.weight * x[i]
                                            for c in self.clients_to_be_visited)
                                <= self.problem_instance.drone.max_weight,
                                name=f"weight_constr_f{i}")

            model.optimize()

            for i in range(len(x)):
                if x[i].X > 0.5:
                    flights.append(all_flights[i])
        else:
            for c in self.clients_to_be_visited:
                flights.append(Flight(self.start_node, self.end_node, [c], self.problem_instance.drone))

        return flights
