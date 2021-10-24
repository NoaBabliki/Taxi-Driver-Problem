
import taxi_problem_solver as tps
import build_map

import random

import matplotlib.pyplot as plt

NUM_OF_PASSENGERS = 8

BRUTE_FORCE = tps.BruteForceSolver
GREEDY = tps.GreedyTaxiProblemSolver
RANDOM = tps.RandomTaxiProblemSolver

SIMULATED_ANNEALING = tps.SimulatedAnnealingTaxiProblemSolver
HILL_CLIMBING = tps.HillClimbingTaxiProblemSolver
LOCAL_SEARCH = tps.LocalSearchTaxiProblemSolver
BEAM = tps.BeamLocalSearchTaxiProblemSolver
MULTIPLE = tps.MultipleLocalSearchTaxiProblemSolver


def onclick(fig_context):
    fig, cur_sol, steps_for_demo, cid = fig_context
    fig.clear()
    solution, cur_dist = steps_for_demo[cur_sol]
    print(solution)

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
        fig.canvas.mpl_disconnect(cid)
        ax.set_title("Final Solution Length: " + str(round(cur_dist, 2)))

    fig_context[1] = cur_sol + 1
    plt.draw()



def demo_local_search_with_greedy_as_baseline(passengers):
    rand = GREEDY(passengers, (0, 0))
    solution_greedy = rand.solve()


    local_search = LOCAL_SEARCH(passengers, (0, 0), solution_greedy)
    _, steps_for_demo = local_search.solve()

    # print('first: ', steps_for_demo[0][-1])
    # print('last: ', steps_for_demo[-1][-1])
    print('diff: ', steps_for_demo[0][-1] - steps_for_demo[-1][-1])
    print('len: ', len(steps_for_demo))
    print()


    fig = plt.figure()
    fig_context = [fig, 0, steps_for_demo, None]
    onclick(fig_context)
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(fig_context))
    fig_context[3] = cid
    plt.show()


if __name__ == "__main__":
    # for i in range(200):
    #     print('i = ', i)
    random.seed(181)
    passengers = build_map.build_map_of_passengers(NUM_OF_PASSENGERS)
    demo_local_search_with_greedy_as_baseline(passengers)
