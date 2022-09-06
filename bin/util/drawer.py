from matplotlib import pyplot as plt
from bin.problem_instantiator import ProblemInstance
from bin.util.optimal_solution import OptimalSolution
from bin.util.rts_solution import RTSSolution


def draw_solution(problem_instance: ProblemInstance, solution, space_dimension: int):
    if not solution.is_infeasible:
        plt.rcParams["figure.figsize"] = [9.00, 7.50]
        plt.rcParams["figure.autolayout"] = True
        plt.xlim(0, space_dimension)
        plt.ylim(0, space_dimension)
        plt.grid()
        for v in problem_instance.travel_nodes:
            if v.is_warehouse:
                plt.plot(v.x_coordinate, v.y_coordinate, marker="s", markersize=6, markeredgecolor="blue",
                         markerfacecolor="blue", alpha=0.8)
            else:
                plt.plot(v.x_coordinate, v.y_coordinate, marker="o", markersize=5, markeredgecolor="blue",
                         markerfacecolor="blue")
            plt.text(v.x_coordinate + space_dimension / 100, v.y_coordinate + space_dimension / 100,
                     f"V{v.index}", fontsize="medium", color="blue")
        for c in problem_instance.client_nodes:
            plt.plot(c.x_coordinate, c.y_coordinate, marker="o", markersize=5, markeredgecolor="red",
                     markerfacecolor="red", alpha=0.8)
            plt.text(c.x_coordinate + space_dimension / 100, c.y_coordinate + space_dimension / 100,
                     f"C{c.index}", fontsize="medium", color="red")
            plt.text(c.x_coordinate + space_dimension / 100, c.y_coordinate - space_dimension / 100,
                     f"{round(c.weight,1)}kg", fontsize="small", color="red", alpha=0.5)

        if type(solution) == RTSSolution:
            for e in solution.active_edges:
                o = e.operation
                plt.arrow(o.start_node.x_coordinate, o.start_node.y_coordinate,
                          o.end_node.x_coordinate - o.start_node.x_coordinate,
                          o.end_node.y_coordinate - o.start_node.y_coordinate,
                          head_width=space_dimension / 120, head_length=space_dimension / 60,
                          length_includes_head=True, color="blue", alpha=0.5)
                for flight in o.flights:
                    if flight.list_of_movements:
                        for movement in flight.list_of_movements:
                            plt.arrow(movement.start_node.x_coordinate, movement.start_node.y_coordinate,
                                      movement.end_node.x_coordinate - movement.start_node.x_coordinate,
                                      movement.end_node.y_coordinate - movement.start_node.y_coordinate,
                                      head_width=space_dimension / 140, head_length=space_dimension / 70,
                                      length_includes_head=True,
                                      color="red", linestyle="dotted", alpha=0.3)
        elif type(solution) == OptimalSolution:
            for o in solution.operations:
                plt.arrow(o.start_node.x_coordinate, o.start_node.y_coordinate,
                          o.end_node.x_coordinate - o.start_node.x_coordinate,
                          o.end_node.y_coordinate - o.start_node.y_coordinate,
                          head_width=space_dimension / 120, head_length=space_dimension / 60,
                          length_includes_head=True, color="blue", alpha=0.5)
                for flight in o.flights:
                    if flight.list_of_movements:
                        for movement in flight.list_of_movements:
                            plt.arrow(movement.start_node.x_coordinate, movement.start_node.y_coordinate,
                                      movement.end_node.x_coordinate - movement.start_node.x_coordinate,
                                      movement.end_node.y_coordinate - movement.start_node.y_coordinate,
                                      head_width=space_dimension / 140, head_length=space_dimension / 70,
                                      length_includes_head=True,
                                      color="red", linestyle="dotted", alpha=0.3)
        algorithm = "RTS" if type(solution) == RTSSolution else "OPT"
        plt.suptitle(f"drone speed: {problem_instance.drone.speed}m/s  "
                     f"max energy: {problem_instance.drone.max_energy_available}J  "
                     f"k: {problem_instance.number_of_available_drones}  "
                     f"algorithm: {algorithm}")
        plt.show()
