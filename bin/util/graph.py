from bin.nodes.client_node import ClientNode
from bin.nodes.travel_node import TravelNode
from bin.operations.operation import Operation
from bin.problem_instantiator import ProblemInstance
from bin.util.operation_builder import OperationBuilder
from bin.util.operation_builder_modified import OperationBuilderV2


class GraphNode:
    def __init__(self, travel_node: TravelNode, number_of_serviced_clients):
        self.travel_node = travel_node
        self.number_of_serviced_clients = number_of_serviced_clients

    def __str__(self):
        return "[" + str(self.travel_node.index) + ", " + str(self.number_of_serviced_clients) + "]"


class GraphEdge:
    def __init__(self, first_node: GraphNode, second_node: GraphNode, operation: Operation):
        self.first_node = first_node
        self.second_node = second_node
        self.operation = operation
        self.cost = self.compute_edge_cost()

    def compute_edge_cost(self):
        return self.operation.compute_operation_time()

    def __str__(self):
        return "[" + str(self.first_node) + ", " + str(self.second_node) + ", " + str(self.cost) + "]"


class Graph:
    def __init__(self, problem_instance: ProblemInstance, visit_order: list[ClientNode], modified_op_builder=False):
        self.problem_instance = problem_instance
        self.visit_order = visit_order
        self.use_modified_op_builder = modified_op_builder
        self.nodes = self.build_nodes()
        self.edges = self.build_edges()

    def build_nodes(self):
        nodes = []
        for i in range(len(self.problem_instance.travel_nodes)):
            row = []
            for j in range(len(self.problem_instance.client_nodes) + 1):
                row.append(GraphNode(self.problem_instance.travel_nodes[i], j))
            nodes.append(row)
        return nodes

    def build_edges(self):
        edges = []
        for i in range(len(self.problem_instance.travel_nodes)):
            for j in range(len(self.problem_instance.client_nodes)):
                edges_computed = self.compute_all_edges_for_node(self.nodes[i][j])
                for edge in edges_computed:
                    edges.append(edge)
        return edges

    def compute_all_edges_for_node(self, starting_node: GraphNode):
        edges_computed = []
        for i in range(len(self.nodes)):
            for j in range(starting_node.number_of_serviced_clients, len(self.nodes[i])):
                if i != starting_node.travel_node.index or j != starting_node.number_of_serviced_clients:
                    if self.use_modified_op_builder:
                        operation_builder = OperationBuilderV2(self.problem_instance, starting_node.travel_node,
                                                               self.nodes[i][j].travel_node,
                                                               self.nodes[i][j].number_of_serviced_clients,
                                                               starting_node.number_of_serviced_clients,
                                                               self.visit_order)
                    else:
                        operation_builder = OperationBuilder(self.problem_instance, starting_node.travel_node,
                                                             self.nodes[i][j].travel_node,
                                                             self.nodes[i][j].number_of_serviced_clients,
                                                             starting_node.number_of_serviced_clients,
                                                             self.visit_order)
                    op = operation_builder.build_operation()
                    if op:
                        edges_computed.append(GraphEdge(starting_node, self.nodes[i][j], op))
        return edges_computed

    def get_outgoing_edges_indexes(self, node: GraphNode):
        indexes = []
        for edge in self.edges:
            if edge.first_node == node:
                indexes.append(self.edges.index(edge))
        return indexes

    def get_entering_edges_indexes(self, node: GraphNode):
        indexes = []
        for edge in self.edges:
            if edge.second_node == node:
                indexes.append(self.edges.index(edge))
        return indexes

    def get_start_node(self):
        return self.nodes[self.problem_instance.get_warehouse().index][0]

    def get_end_node(self):
        return self.nodes[self.problem_instance.get_warehouse().index][len(self.problem_instance.client_nodes)]

    def __str__(self):
        s = ""
        for e in self.edges:
            s += str(e) + "\n"
        return s
