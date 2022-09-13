from bin.util.graph import GraphEdge


class RTSSolution:
    def __init__(self, is_infeasible: bool, total_time: float,
                 active_edges: list[GraphEdge], computational_time: float, tsp_obj: float):
        self.is_infeasible = is_infeasible
        if not self.is_infeasible:
            self.total_time = total_time
            self.active_edges = active_edges
            self.computational_time = computational_time
            self.tsp_obj_value = tsp_obj
        else:
            self.total_time = 0
            self.active_edges = None
            self.computational_time = 0
            self.tsp_obj_value = 0
