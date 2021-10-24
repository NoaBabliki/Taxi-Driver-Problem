import argparse
import taxi_problem_solver as tps
import build_map
import genetic_algorithm_solver as gf
import random
from local_search_from_RANDOM_demo import demo_local_search_with_random_as_baseline
import utils

import matplotlib.pyplot as plt
import genetic_functions_keep_sorted as gf_keep_sorted

from genetic_funcs_interface import GeneticFuncsInterface

EPSILON = 0.0000001

BRUTE_FORCE = tps.BruteForcePruningSolver
GREEDY = tps.GreedyTaxiProblemSolver
RANDOM = tps.RandomTaxiProblemSolver

SIMULATED_ANNEALING = tps.SimulatedAnnealingTaxiProblemSolver
HILL_CLIMBING = tps.HillClimbingTaxiProblemSolver
LOCAL_SEARCH = tps.LocalSearchTaxiProblemSolver
BEAM = tps.BeamLocalSearchTaxiProblemSolver
MULTIPLE = tps.MultipleLocalSearchTaxiProblemSolver

GENETIC = gf.GeneticTaxiProblemSolver

DEFAULT_SEED = 5
DEFAULT_NUM_OF_PASSENGERS = 20


def plot_solution(solution):
    """plots the given solution. Pick up stations in blue, drop stations in red"""
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x, y, z = [p[0][0] for p in solution], [p[0][1] for p in solution], [p[1] for p in solution]
    ax.plot(x, y, 'b-')

    for i in range(len(x)):
        ax.annotate(str(z[i]), (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    x_u, y_u = [p[0][0] for p in solution[1:] if not p[2]], [p[0][1] for p in solution[1:] if not p[2]]
    x_d, y_d = [p[0][0] for p in solution[1:] if p[2]], [p[0][1] for p in solution[1:] if p[2]]
    ax.plot(x_u, y_u, 'bo')
    ax.plot(x_d, y_d, 'rs')

    cur_dist = utils.get_solution_len(solution)
    ax.set_title("Solution Length: " + str(round(cur_dist, 2)))
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Taxi Driver Problem Solver')
    parser.add_argument('-n', '--num_of_passengers', help='Number of passengers, must be a positive int.',
                        default=DEFAULT_NUM_OF_PASSENGERS, type=int)
    parser.add_argument('-s', '--random_seed', help='The seed for the passengers stations.', default=DEFAULT_SEED,
                        type=int)
    algorithms = ['Greedy', 'LocalSearch', 'HillClimbing', 'SimulatedAnnealing', 'BeamLocalSearch', 'Multiple',
                  'Genetic', 'BruteForce']
    parser.add_argument('-a', '--algorithm', choices=algorithms, help='choose which algorithm to run.',
                        default=algorithms[0], type=str)

    parser.add_argument('-d', '--demo', help='Run demo on Local Search over random solution.', action='store_true')

    args = parser.parse_args()
    random.seed(args.random_seed)
    passengers = build_map.build_map_of_passengers(args.num_of_passengers)

    if args.demo:
        demo_local_search_with_random_as_baseline(passengers)
        return

    if args.num_of_passengers < 7:
        sol_greedy = GREEDY(passengers, (0, 0)).solve()
        greedy_dist = utils.get_solution_len(sol_greedy)
        alg = BRUTE_FORCE(passengers, (0, 0), greedy_dist + EPSILON)
        alg.solve([((0, 0), 0)])
        s = alg.best_solution
        print(s)
        plot_solution(s)
        return

    if args.algorithm == 'Genetic':
        funcs = GeneticFuncsInterface(gf_keep_sorted.crossover_keep_sorted, gf_keep_sorted.mutation_keep_sorted)
        alg = GENETIC(passengers, (0, 0), funcs)
        s, _ = alg.solve()
    elif args.algorithm == 'LocalSearch':
        sol_greedy = GREEDY(passengers, (0, 0)).solve()
        alg = LOCAL_SEARCH(passengers, (0, 0), sol_greedy)
        s, _ = alg.solve()
    elif args.algorithm == 'BruteForce':
        sol_greedy = GREEDY(passengers, (0, 0)).solve()
        greedy_dist = utils.get_solution_len(sol_greedy)
        alg = BRUTE_FORCE(passengers, (0, 0), greedy_dist + EPSILON)
        alg.solve([((0, 0), 0)])
        s = alg.best_solution
    else:
        sol_greedy = GREEDY(passengers, (0, 0)).solve()
        if args.algorithm == 'Greedy':
            alg = GREEDY(passengers, (0, 0))
        elif args.algorithm == 'HillClimbing':
            alg = HILL_CLIMBING(passengers, (0, 0), sol_greedy)
        elif args.algorithm == 'SimulatedAnnealing':
            alg = SIMULATED_ANNEALING(passengers, (0, 0), sol_greedy)
        elif args.algorithm == 'BeamLocalSearch':
            alg = BEAM(passengers, (0, 0), sol_greedy)
        elif args.algorithm == 'Multiple':
            sol_random = RANDOM(passengers, (0, 0)).solve()
            alg = MULTIPLE(passengers, (0, 0), sol_random, 100)

        s = alg.solve()

    print(s)
    plot_solution(s)


if __name__ == "__main__":
    main()
