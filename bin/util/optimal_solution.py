from bin.operations.operation import Operation


class OptimalSolution:
    def __init__(self, is_infeasible: bool, total_time: float,
                 operations: list[Operation], computational_time: float):
        self.is_infeasible = is_infeasible
        if not self.is_infeasible:
            self.total_time = total_time
            self.operations = operations
            self.computational_time = computational_time
        else:
            self.total_time = 0
            self.operations = None
            self.computational_time = 0
