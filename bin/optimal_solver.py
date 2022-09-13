import time

from bin.nodes.client_node import ClientNode
from bin.nodes.travel_node import TravelNode
from bin.operations.flight import Flight
from bin.operations.movement import Movement
from bin.operations.operation import Operation
from bin.problem_instantiator import ProblemInstance
import itertools
import gurobipy as gb

from bin.util.optimal_solution import OptimalSolution


def cover(operation: Operation, client: ClientNode):
    for flight in operation.flights:
        if client in flight.visited_clients:
            return 1
    return 0


def rp(operation: Operation, node: TravelNode):
    return operation.start_node == node


def lp(operation: Operation, node: TravelNode):
    return operation.end_node == node


def wp(operation: Operation, start_node: TravelNode, end_node: TravelNode):
    return operation.start_node == start_node and operation.end_node == end_node


class OptimalSolver:

    def __init__(self, problem_instance: ProblemInstance):
        self.problem_instance = problem_instance
        self.start_time = time.time()
        self.feasible_flights = []
        self.all_feasible_operations = self.compute_all_feasible_operations()
        self.x = []

    def compute_all_feasible_truck_movements(self):
        all_feasible_truck_movements = []
        for start_node in self.problem_instance.travel_nodes:
            for end_node in self.problem_instance.travel_nodes:
                all_feasible_truck_movements.append(Movement(start_node, end_node, self.problem_instance.truck))
        return all_feasible_truck_movements

    # noinspection PyTypeChecker
    def compute_all_feasible_operations(self):
        operations_computed = []
        pointer = 0
        for movement in self.compute_all_feasible_truck_movements():
            ops = []
            if movement.start_node != movement.end_node:
                ops.append(Operation(self.problem_instance, movement.start_node, movement.end_node,
                                     [], self.problem_instance.truck))
            self.compute_all_feasible_flights(Flight(movement.start_node,
                                                     movement.end_node,
                                                     [],
                                                     self.problem_instance.drone))
            flights = []
            for i in range(pointer, len(self.feasible_flights)):
                ops.append(Operation(self.problem_instance, self.feasible_flights[i].takeoff_node,
                                     self.feasible_flights[i].landing_node,
                                     [self.feasible_flights[i]], self.problem_instance.truck))
            for i in range(pointer, len(self.feasible_flights)):
                flights.append(self.feasible_flights[i])
            for n in range(2, self.problem_instance.number_of_available_drones + 1):
                combinations = itertools.combinations(flights, n)
                for flights_comb in combinations:
                    ops.append(Operation(self.problem_instance, movement.start_node, movement.end_node,
                                         flights_comb, self.problem_instance.truck))
            pointer = len(self.feasible_flights)
            for operation in ops:
                operations_computed.append(operation)
        return operations_computed

    def compute_all_feasible_flights(self, flight):
        computed_flights = self.compute_feasible_steps(flight)
        if computed_flights:
            for flight in computed_flights:
                self.feasible_flights.append(flight)
                self.compute_all_feasible_flights(flight)

    def compute_feasible_steps(self, flight):
        feasible_flights_computed = []
        for client in self.problem_instance.client_nodes:
            visited_clients = flight.visited_clients.copy()
            if client not in visited_clients:
                visited_clients.append(client)
                new_flight = Flight(flight.takeoff_node, flight.landing_node, visited_clients, flight.drone)
                if new_flight.compute_energy_used_for_flight(self.problem_instance) < flight.drone.max_energy_available:
                    feasible_flights_computed.append(new_flight)
        return feasible_flights_computed

    def solve(self):
        env = gb.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        model = gb.Model(env=env)
        times = []
        o = self.all_feasible_operations
        for i in range(len(o)):
            self.x.append(model.addVar(vtype=gb.GRB.BINARY, name=f"x[{i}]"))
            times.append(o[i].compute_operation_time())

        model.modelSense = gb.GRB.MINIMIZE
        model.setObjective(gb.quicksum(times[i] * self.x[i] for i in range(len(self.x))))

        for client in self.problem_instance.client_nodes:
            model.addConstr(gb.quicksum(cover(o[i], client) * self.x[i] for i in range(len(self.x))) >= 1,
                            name=f"client_constraint{client.index}")

        for travel_node in self.problem_instance.travel_nodes:
            model.addConstr(gb.quicksum(rp(o[i], travel_node) * self.x[i] for i in range(len(self.x))) -
                            gb.quicksum(lp(o[i], travel_node) * self.x[i] for i in range(len(self.x)))
                            == 0, name=f"travel_constraint{travel_node.index}")

        model.addConstr(gb.quicksum(rp(o[i], self.problem_instance.get_warehouse()) * self.x[i]
                                    for i in range(len(self.x))) >= 1,
                        name="CO")
        model.addConstr(gb.quicksum(lp(o[i], self.problem_instance.get_warehouse()) * self.x[i]
                                    for i in range(len(self.x))) >= 1,
                        name="C1")

        for sets in self.compute_set():
            for set_of_nodes in sets:
                model.addConstr(
                    gb.quicksum(
                        gb.quicksum(
                            gb.quicksum(wp(o[i], v1, v2) * self.x[i] for i in range(len(self.x)))
                            for v2 in set_of_nodes
                        )
                        for v1 in set_of_nodes
                    ) <= len(set_of_nodes) - 1,
                    name="subtour_elim"
                )

        for v1 in self.get_partial_travel_nodes_set(self.problem_instance.get_warehouse()):
            model.addConstr(
                gb.quicksum(
                    gb.quicksum(
                        wp(o[i], v1, v2) * self.x[i] for i in range(len(o))
                    ) for v2 in self.get_partial_travel_nodes_set(v1)
                ) * self.cp(v1) - self.cp(v1) >= 0,
                name="circle_elim"
            )

        model.optimize()

        is_infeasible = model.Status == gb.GRB.INFEASIBLE
        operations = []
        total_time = 0
        if not is_infeasible:
            total_time = model.ObjVal
            for i in range(len(self.x)):
                if self.x[i].X > 0.5:
                    operations.append(o[i])

        return OptimalSolution(is_infeasible, total_time, operations, time.time() - self.start_time)

    def compute_set(self):
        computed_set = []
        travel_nodes = self.problem_instance.travel_nodes.copy()
        travel_nodes.remove(self.problem_instance.get_warehouse())
        for n in range(2, len(self.problem_instance.travel_nodes) - 1):
            computed_set.append(set(itertools.permutations(travel_nodes, n)))
        return computed_set

    def get_partial_travel_nodes_set(self, node_to_remove):
        travel_node = self.problem_instance.travel_nodes.copy()
        travel_node.remove(node_to_remove)
        return travel_node

    def cp(self, node: TravelNode):
        return gb.quicksum(rp(self.all_feasible_operations[i], node) * lp(self.all_feasible_operations[i], node) *
                           self.x[i] for i in range(len(self.all_feasible_operations)))
