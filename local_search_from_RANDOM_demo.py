import taxi_problem_solver as tps
import build_map
import matplotlib.pyplot as plt

NUM_OF_PASSENGERS = 20

BRUTE_FORCE = tps.BruteForceSolver
GREEDY = tps.GreedyTaxiProblemSolver
RANDOM = tps.RandomTaxiProblemSolver

SIMULATED_ANNEALING = tps.SimulatedAnnealingTaxiProblemSolver
HILL_CLIMBING = tps.HillClimbingTaxiProblemSolver
LOCAL_SEARCH = tps.LocalSearchTaxiProblemSolver
BEAM = tps.BeamLocalSearchTaxiProblemSolver
MULTIPLE = tps.MultipleLocalSearchTaxiProblemSolver


def onclick(fig_context):
    """plot the solution and then, on click, it shows the next step of the algorithm"""
    fig, cur_sol, steps_for_demo = fig_context
    fig.clear()
    solution, cur_dist = steps_for_demo[cur_sol]
    ax = fig.add_subplot(111)
    x, y, z = [p[0][0] for p in solution], [p[0][1] for p in solution], [p[1] for p in solution]
    ax.plot(x, y, 'b-')

    for i in range(len(x)):
        ax.annotate(str(z[i]), (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    x_u, y_u = [p[0][0] for p in solution[1:] if not p[2]], [p[0][1] for p in solution[1:] if not p[2]]
    x_d, y_d = [p[0][0] for p in solution[1:] if p[2]], [p[0][1] for p in solution[1:] if p[2]]

    ax.plot(x_u, y_u, 'bo')
    ax.plot(x_d, y_d, 'rs')

    ax.set_title("Solution Length: " + str(round(cur_dist, 2)))

    if cur_sol == len(steps_for_demo) - 1:
        ax.set_title("Final Solution Length: " + str(round(cur_dist, 2)))

    fig_context[1] = cur_sol + 1
    plt.draw()


def demo_local_search_with_random_as_baseline(passengers):
    """
    plots the rout given by LocalSearch algorithm step by step
    :param passengers: list of passengers
    :return: None
    """
    rand = RANDOM(passengers, (0, 0), None)
    solution_greedy = rand.solve()

    local_search = LOCAL_SEARCH(passengers, (0, 0), solution_greedy)
    _, steps_for_demo = local_search.solve()

    fig = plt.figure()
    fig_context = [fig, 0, steps_for_demo]

    for k in range(len(steps_for_demo)):
        onclick(fig_context)
        if k < 10:
            plt.pause(0.1)
        elif k < 20:
            plt.pause(0.06)
        else:
            plt.pause(0.02)

    plt.show()


if __name__ == "__main__":
    passengers = build_map.build_map_of_passengers(NUM_OF_PASSENGERS)
    demo_local_search_with_random_as_baseline(passengers)
